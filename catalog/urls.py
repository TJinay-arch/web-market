# catalog/urls.py
from django.urls import path

from .views import CatalogView, ContactsView, ProductDetailsView

app_name = "catalog"

urlpatterns = [
    path("home/", CatalogView.as_view(), name="home"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("catalog/products/<int:pk>/", ProductDetailsView.as_view(), name="catalog_details_about_product"),
]
