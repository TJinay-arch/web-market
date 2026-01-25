from django import forms
from django.core.exceptions import ValidationError

from .models import Product
import re


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=20)
    message = forms.CharField(widget=forms.Textarea)


FORBIDDEN_WORDS = [
    "казино", "криптовалюта", "крипта", "биржа", "дешево",
    "бесплатно", "обман", "полиция", "радар"
]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if any(re.search(r'\b{}\b'.format(word), name, re.IGNORECASE) for word in FORBIDDEN_WORDS):
            raise ValidationError("Наименование содержит недопустимые слова.")
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if any(re.search(r'\b{}\b'.format(word), description, re.IGNORECASE) for word in FORBIDDEN_WORDS):
            raise ValidationError("Описание содержит недопустимые слова.")
        return description

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise ValidationError("Укажите корректную цену.")
        return price

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible_field in self.visible_fields():
            visible_field.field.widget.attrs.update({
                'class': 'form-control'
            })

        self.fields['name'].widget.attrs.update({'placeholder': 'Название продукта'})
        self.fields['description'].widget.attrs.update({'rows': 4})
        self.fields['price'].widget.attrs.update({'step': '0.01', 'min': '0'})
