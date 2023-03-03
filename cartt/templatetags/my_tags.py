from django import template
from django.shortcuts import redirect
from django.urls import reverse

register = template.Library()

@register.filter
def multiply(value, arg):
    """Умножает значение на заданный аргумент."""
    return value * arg


