from django.db import models

class Phone(models.Model):
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.CharField(max_length=150)
    specifications = models.TextField()
    image = models.ImageField(upload_to='phones', blank=True, null=True)

    def __str__(self):
        return f'{self.brand} {self.model}'