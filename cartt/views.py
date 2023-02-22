from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from catalog.models import CartItems, Basket, Orders
from catalog.models import Phone
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText




@login_required
def cart_add(request, phone_id):
    phone = get_object_or_404(Phone, id=phone_id)
    cart = Basket.objects.filter(user=request.user).last()
    if not cart:
        cart = Basket.objects.create(user=request.user)
    cart_item, created = CartItems.objects.get_or_create(cart=cart, item=phone)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart_detail')


@login_required
def cart_detail(request):
    cart = Basket.objects.filter(user=request.user).last()
    if not cart:
        return render(request, 'cart/detail.html', {'cart_items': []})
    cart_items = cart.items.all()
    total_price = sum(item.item.price * item.quantity for item in cart_items)
    return render(request, 'cart/detail.html', {'cart_items': cart_items, 'total_price': total_price})


@require_POST
@login_required
def cart_update(request, item_id):
    cart_item = get_object_or_404(CartItems, id=item_id, cart__user=request.user)
    action = request.POST.get('action')
    if action == 'increment':
        cart_item.quantity += 1
    elif action == 'decrement':
        cart_item.quantity -= 1
        if cart_item.quantity <= 0:
            cart_item.delete()
            return redirect('cart_detail')
    elif action == 'delete':
        cart_item.delete()
        return redirect('cart_detail')
    cart_item.save()
    return redirect('cart_detail')


def send_order_email(email, order_id, items, total_price):
    # Конфигурация SMTP сервера
    smtp_host = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'mishagon02@gmail.com'
    smtp_password = 'nchhfimsvyarssib'
    smtp_sender = 'mishagon02@gmail.com'

    # Создание сообщения
    message = MIMEMultipart()
    message['From'] = smtp_sender
    message['To'] = email
    message['Subject'] = f'Заказ №{order_id}'

    # Создание текстового сообщения
    text = f'Ваш заказ №{order_id} подтвержден!\n\n Заказанные товары:\n\n'
    for item in items:
        text += f'{item["name"]} ({item["description"]}) - {item["price"]} руб. x {item["quantity"]}\n'
    text += f'\nИтоговая сумма: {total_price} руб.\n\nСпасибо, что выбрали наш магазин!\n\n'
    message.attach(MIMEText(text))

    # Отправка сообщения
    try:
        with smtplib.SMTP(smtp_host, smtp_port) as smtp:
            smtp.starttls()
            smtp.login(smtp_username, smtp_password)
            smtp.sendmail(smtp_sender, email, message.as_string())
        print(f'Message has been sent to {email}')
    except Exception as e:
        print(f'Error sending message to {email}: {e}')





def create_order(request):
    if request.method == 'POST':
        basket = Basket.objects.get(user=request.user)
        cart_items = CartItems.objects.filter(cart=basket)
        email = request.POST.get('email')
        items = [{'name': str(item.item), 'description': str(item.item.description), 'price': item.item.price, 'quantity': item.quantity} for item in cart_items]
        total_price = sum(item.item.price * item.quantity for item in cart_items)
        address = request.POST.get('address')
        is_deliver = True if address else False
        order = Orders.objects.create(user_id=request.user.id, email=email, items=items, address=address, total_price=total_price, is_deliver=is_deliver)
        order.save()
        cart_items.delete()
        send_order_email(email, order.id, items, total_price)
        return render(request, 'cart/order_success.html', {'order_id': order.id})

    else:
        return render(request, 'cart/order.html')


