from django.http import Http404, HttpResponse
from django.shortcuts import render

from .models import Category, ContactInfo, Product


def catalog_contacts_view(request):
    contacts = ContactInfo.objects.all()
    if request.method == "POST":
        # Получение данных из формы
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        # Обработка данных (например, сохранение в БД, отправка email и т.д.)
        print(name, phone, message)
        # Здесь мы просто возвращаем простой ответ
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено. Мы свяжемся с вами в ближайшее время.")
    return render(request, "catalog/contacts.html", {"contacts": contacts})


def catalog_view(request):
    # Получаем все категории и заранее подгружаем связанные товары
    categories = Category.objects.prefetch_related("products").all()

    # Формируем словарь, где ключ — категория, а значение — список товаров
    products_by_categories = {}
    for category in categories:
        products_by_categories[category] = Product.objects.filter(category=category)

    # Готовим контекст для шаблона
    context = {"categories": categories, "products_by_categories": products_by_categories}

    return render(request, "catalog/home.html", context)


def catalog_details_about_product(request, product_id):
    try:
        # Прямой выбор товара по переданному id
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        # Обрабатываем случай отсутствия товара с таким id
        raise Http404("Товар не найден")

    context = {"product": product}
    return render(request, "catalog/details_about_product.html", context)
