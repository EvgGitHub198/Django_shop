from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from catalog.forms import SearchForm
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
    return render(request, 'catalog/phone_detail.html', {'phone': phone})


def search_view(request):
    query = request.GET.get('q')
    if query:
        products = Phone.objects.filter(Q(brand__icontains=query) | Q(model__icontains=query) | Q(description__icontains=query))
    else:
        products = Phone.objects.all()
    return render(request, 'catalog/search.html', {'products': products})
