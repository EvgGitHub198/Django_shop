from django.shortcuts import render
from datetime import datetime

from gallery.models import Image


def home(request):
    images = Image.objects.all()
    return render(request, 'home.html', {'images': images})


def base(request):
    context = {
        'year': datetime.now().year,
    }
    return render(request, 'base.html', context)

