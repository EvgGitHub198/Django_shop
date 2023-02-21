from django.urls import path
from .views import cart_add, cart_detail, cart_update, create_order

urlpatterns = [
    path('', cart_detail, name='cart_detail'),
    path('add/<int:phone_id>/', cart_add, name='cart_add'),
    path('update/<int:item_id>/', cart_update, name='cart_update'),
    path('order/', create_order, name='order'),
]


