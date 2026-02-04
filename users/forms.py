from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'avatar', 'phone_number', 'username', 'country')
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'Введите почту',
                'class': 'form-control'
            }),
            'username': forms.TextInput(attrs={
                'placeholder': 'Например: Ilya',
                'class': 'form-control'
            }),
            'phone_number': forms.TextInput(attrs={
                'placeholder': 'Например: +79991234567',
                'class': 'form-control'
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control'
            }),
        }
        error_messages = {
            'email': {'unique': 'Этот email уже зарегистрирован.'}
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем класс form-control для avatar
        self.fields['avatar'].widget.attrs.update({'class': 'form-control'})

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            if avatar.size > 2 * 1024 * 1024:
                raise forms.ValidationError('Изображение не должно превышать 2 МБ.')
            if not avatar.content_type.startswith('image/'):
                raise forms.ValidationError('Файл должен быть изображением.')
        return avatar


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем класс form-control для avatar
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Например: Ilya'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})
