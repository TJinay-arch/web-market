from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CustomUserCreationForm, LoginForm


class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = "users/login.html"
    success_url = reverse_lazy("catalog:home")

    def get_success_url(self):
        return self.success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Вход"
        return context


class CustomLogoutView(LogoutView):
    template_name = "users/logout.html"
    next_page = None


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "users/registration.html"
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        # Сохраняем пользователя
        user = form.save()

        # Отправляем приветственное письмо
        send_mail(
            "Моей любимой женушке",
            f"Здравствуйте, {user.username}! Спасибо за регистрацию.",
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        # Автоматически авторизуем пользователя
        login(self.request, user)

        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Регистрация"
        return context
