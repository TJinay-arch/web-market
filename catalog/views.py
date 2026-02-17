from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, ListView, CreateView, DeleteView, UpdateView, View

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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/update_product.html"
    success_url = "/catalog/home/"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.owner != self.request.user:
            raise PermissionDenied('Вы не имеете права редактировать этот продукт')
        return obj


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "catalog/delete_product.html"
    success_url = reverse_lazy("catalog:home")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        is_owner = obj.owner == self.request.user
        is_moderator = self.request.user.has_perm("catalog.delete_product")
        if not (is_owner or is_moderator):
            raise PermissionDenied('Вы не имеете права удалить этот продукт')
        return obj

class ProductUnpublishView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "catalog.can_unpublish_product"
    raise_exception = True

    def post(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            if product.is_published:
                product.is_published = False
                product.save()
                return HttpResponseRedirect(reverse_lazy("catalog:catalog_details_about_product", kwargs={"pk": pk}))
            else:
                return HttpResponse("Продукт уже не опубликован.", status=400)
        except Product.DoesNotExist:
            raise Http404("Продукт не найден.")
