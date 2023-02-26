from django.core.paginator import Paginator
from django.db import models
from django.shortcuts import render, get_object_or_404, redirect

from catalog.forms import SearchForm, ReviewForm
from catalog.models import Phone
from django.db.models import Q


def phone_list(request):
    phone_list = Phone.objects.all()
    paginator = Paginator(phone_list, 8)  # количество объектов на странице

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
