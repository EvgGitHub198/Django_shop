from django.urls import path
from .views import phone_detail, phone_list, search_view

urlpatterns = [
    path('phones/', phone_list, name='phone_list'),
    path('phone/<int:pk>/', phone_detail, name='phone_detail'),
    path('search/', search_view, name='search'),

]
