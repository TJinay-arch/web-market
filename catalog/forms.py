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
        fields = ['name', 'description', 'image', 'category', 'price', 'is_published']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # Поле is_published доступно только владельцу при редактировании или модератору
        if not self.user:
            # Если пользователь не передан, скрываем поле
            self.fields.pop('is_published', None)
        elif not self.instance.pk:
            # При создании нового продукта скрываем поле (по умолчанию False)
            self.fields.pop('is_published', None)
        elif self.instance.owner != self.user:
            # Если редактируем чужой продукт и не модератор, скрываем поле
            if not self.user.has_perm('catalog.can_unpublish_product'):
                self.fields.pop('is_published', None)

        for visible_field in self.visible_fields():
            visible_field.field.widget.attrs.update({
                'class': 'form-control'
            })

        self.fields['name'].widget.attrs.update({'placeholder': 'Название продукта'})
        self.fields['description'].widget.attrs.update({'rows': 4})
        self.fields['price'].widget.attrs.update({'step': '0.01', 'min': '0'})
        if 'is_published' in self.fields:
            self.fields['is_published'].widget.attrs.update({'class': 'form-check-input'})

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

