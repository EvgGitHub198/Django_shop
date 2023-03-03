from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import models
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from catalog.forms import ReviewForm
from catalog.models import Phone, Basket, CartItems
from django.db.models import Q, Sum


def phone_list(request):
    phone_list = Phone.objects.all()
    paginator = Paginator(phone_list, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'phones': page_obj,
    }
    return render(request, 'catalog/phone_list.html', context)


def phone_detail(request, pk):
    phone = get_object_or_404(Phone, pk=pk)
    reviews = phone.reviews.all()
    average_rating = reviews.aggregate(models.Avg('rating'))['rating__avg']
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.phone = phone
            review.save()
            return redirect(phone.get_absolute_url())
    return render(request, 'catalog/phone_detail.html', {
        'phone': phone,
        'reviews': reviews,
        'average_rating': average_rating,
        'form': form,
    })

def search_view(request):
    query = request.GET.get('q')
    if query:
        products = Phone.objects.filter(Q(brand__icontains=query) | Q(model__icontains=query) | Q(description__icontains=query))
    else:
        products = Phone.objects.all()
    return render(request, 'catalog/search.html', {'products': products})



def cart_count(request):
    cart_count = 0
    total_items = 0
    if request.user.is_authenticated:
        baskets = Basket.objects.filter(user=request.user)
        if baskets.exists():
            cart_count = baskets[0].items.count()
            total_items = CartItems.objects.filter(cart__user=request.user).aggregate(total_items=Sum('quantity'))['total_items'] or 0
    return {'cart_count': cart_count, 'total_items': total_items if total_items else 0}
