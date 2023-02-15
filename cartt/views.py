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
    cart_items = CartItems.objects.all()
    total_price = sum(item.item.price * item.quantity for item in cart_items)
    return render(request, 'cart/detail.html', {'cart_items': cart_items, 'total_price': total_price})



# def cart_detail(request):
#     cart_items = CartItems.objects.all()
#     total_price = sum(item.item.price * item.quantity for item in cart_items)
#     return render(request, 'cart/detail.html', {'cart_items': cart_items, 'total_price': total_price})

