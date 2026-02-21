from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, ListView, CreateView, DeleteView, UpdateView, View
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from .services import get_products_by_category
from django.core.cache import cache

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

@method_decorator(cache_page(60 * 15), name='dispatch')
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
        obj = form.save(commit=False)
        form.instance.owner = self.request.user
        if self.request.POST.get("add"):
            obj.is_published = False
        else:
            obj.is_published = True
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

class CategoryProductsView(ListView):
    model = Product
    template_name = "catalog/category_products.html"
    context_object_name = "products"
    paginate_by = 12

    def get_queryset(self):
        category_id = self.kwargs.get("category_id")
        cache_key = f"products_category_{category_id}"
        queryset = cache.get(cache_key)

        if not queryset:
            queryset = get_products_by_category(category_id)
            cache.set(cache_key, queryset, 60 * 15)  # Кешируем на 15 минут

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get("category_id")

        # Кешируем информацию о категории
        cache_key_category = f"category_{category_id}"
        category = cache.get(cache_key_category)

        if not category:
            try:
                category = Category.objects.get(id=category_id)
                cache.set(cache_key_category, category, 60 * 15)
            except Category.DoesNotExist:
                category = None

        context["category"] = category
        return context

