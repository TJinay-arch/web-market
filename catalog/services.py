from .models import Product


def get_products_by_category(category_id):
    try:
        return Product.objects.filter(category_id=category_id, is_published=True)
    except Product.DoesNotExist:
        return Product.objects.none()
