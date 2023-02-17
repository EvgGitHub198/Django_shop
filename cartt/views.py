from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from catalog.models import CartItems, Basket
from catalog.models import Phone
from django.http import JsonResponse





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




# def cart_detail(request):
#     cart_items = CartItems.objects.all()
#     total_price = sum(item.item.price * item.quantity for item in cart_items)
#     return render(request, 'cart/detail.html', {'cart_items': cart_items, 'total_price': total_price})

