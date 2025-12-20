# catalog/urls.py
from django.urls import path
from . import views

app_name = 'example'

urlpatterns = [
    path('home/', views.catalog_home_view, name='catalog_home_view'),
    path('contacts/', views.catalog_contacts_view, name='catalog_contacts_view'),
]
