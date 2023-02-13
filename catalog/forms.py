from ckeditor.widgets import CKEditorWidget
from django import forms
from .models import Phone


class PhoneForm(forms.ModelForm):
    specifications = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Phone
        fields = '__all__'