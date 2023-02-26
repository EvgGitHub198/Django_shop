from django.contrib import admin
from .models import Phone, CartItems, Basket, Orders, Review
from django.db import models
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class PhoneAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorUploadingWidget}
    }


admin.site.register(Phone, PhoneAdmin)
admin.site.register(CartItems)
admin.site.register(Basket)
admin.site.register(Orders)
admin.site.register(Review)
