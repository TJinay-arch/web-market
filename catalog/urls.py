# catalog/urls.py
from django.urls import path

from .views import CatalogView, ContactsView, ProductDetailsView, ProductCreateView, ProductUpdateView, ProductDeleteView

app_name = "catalog"

urlpatterns = [
    path("home/", CatalogView.as_view(), name="home"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("catalog/products/<int:pk>/", ProductDetailsView.as_view(), name="catalog_details_about_product"),
    path("catalog/products/create/", ProductCreateView.as_view(), name="product_create"),
    path("catalog/products/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"),
    path("catalog/products/<int:pk>/delete", ProductDeleteView.as_view(), name="delete_product"),
]
