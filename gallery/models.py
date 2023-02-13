from django.db import models


class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    caption = models.CharField(max_length=100)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.caption