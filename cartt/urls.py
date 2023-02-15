from django.urls import path
from .views import cart_add, cart_detail

urlpatterns = [
    path('', cart_detail, name='cart_detail'),
    path('add/<int:phone_id>/', cart_add, name='cart_add'),
]
