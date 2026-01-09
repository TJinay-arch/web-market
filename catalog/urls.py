# catalog/urls.py
from django.urls import path

from . import views

app_name = "example"

urlpatterns = [
    path("home/", views.catalog_view, name="catalog_home_view"),
    path("contacts/", views.catalog_contacts_view, name="catalog_contacts_view"),
    path(
        "catalog/products/<int:product_id>/", views.catalog_details_about_product, name="catalog_details_about_product"
    ),
]
