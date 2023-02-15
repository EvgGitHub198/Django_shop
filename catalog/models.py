from django.contrib.auth.models import User
from django.db import models

class Phone(models.Model):
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.CharField(max_length=150)
    specifications = models.TextField()
    count = models.IntegerField()
    image = models.ImageField(upload_to='phones', blank=True, null=True)

    def __str__(self):
        return f'{self.brand} {self.model}'


# class Cart(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     items = models.ManyToManyField(Phone, through='CartItems')
#     def __str__(self):
#         return f'{self.user} cart'
#
#
# class CartItems(models.Model):
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
#     item = models.ForeignKey(Phone, on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=1)
#     def __str__(self):
#         return f'{self.item}'


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
