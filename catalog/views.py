from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, ListView, CreateView, DeleteView, UpdateView

from .forms import ContactForm, ProductForm
from .models import Category, ContactInfo, Product


class ContactsView(FormView):
    form_class = ContactForm
    template_name = "catalog/contacts.html"
    success_url = "/thank-you/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Подгружаем контактные данные
        context["contacts"] = ContactInfo.objects.all()
        return context

    def form_valid(self, form):
        data = form.cleaned_data
        name = data.get("name")
        phone = data.get("phone")
        message = data.get("message")
        print(name, phone, message)
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено. Мы свяжемся с вами в ближайшее время.")


class CatalogView(ListView):
    model = Category
    template_name = "catalog/home.html"
    context_object_name = "categories"  # Название переменной в шаблоне

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Формирование словаря "категория → товары"
        products_by_categories = {category: Product.objects.filter(category=category) for category in self.object_list}
        context["products_by_categories"] = products_by_categories
        return context


class ProductDetailsView(DetailView):
    model = Product
    template_name = "catalog/details_about_product.html"
    context_object_name = "product"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if not obj:
            raise Http404("Товар не найден")
        return obj

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/create_product.html"
    success_url = "/catalog/home/"

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/update_product.html"
    success_url = "/catalog/home/"

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "catalog/delete_product.html"
    success_url = reverse_lazy("catalog:home")