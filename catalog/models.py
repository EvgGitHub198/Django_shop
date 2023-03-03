from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Phone(models.Model):
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=150)
    specifications = models.TextField()
    count = models.IntegerField()
    image = models.ImageField(upload_to='phones', blank=True, null=True)

    def __str__(self):
        return f'{self.brand} {self.model}'
    def get_absolute_url(self):
        return reverse('phone_detail', args=[str(self.id)])



class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='baskets')
    def __str__(self):
        return f'{self.user} basket'


class CartItems(models.Model):
    cart = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Phone, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    def __str__(self):
        return f'{self.item}'

class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    email = models.EmailField()
    items = models.TextField()
    address = models.CharField(max_length=400, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_deliver = models.BooleanField(default=False)


    def __str__(self):
        return f'{self.id} | {self.date_created}'


class Review(models.Model):
    phone = models.ForeignKey(Phone, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=255)
    advantages = models.TextField()
    disadvantages = models.TextField()
    comment = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Review by {self.name} for {self.phone}'

