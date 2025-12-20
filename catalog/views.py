from django.shortcuts import render
from django.http import HttpResponse


def catalog_home_view(request):
    return render(request, 'catalog/home.html')


def catalog_contacts_view(request):
    if request.method == 'POST':
        # Получение данных из формы
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        # Обработка данных (например, сохранение в БД, отправка email и т.д.)
        print(name, phone, message)
        # Здесь мы просто возвращаем простой ответ
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено. Мы свяжемся с вами в ближайшее время.")
    return render(request, 'catalog/contacts.html')