from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Add test products to the database.'

    def handle(self, *args, **options):
        # Очистка текущих данных
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Загрузка тестовых данных
        call_command('loaddata', 'catalog/fixtures/category_fixture.json')
        call_command('loaddata', 'catalog/fixtures/product_fixture.json')

        self.stdout.write(self.style.SUCCESS("Тестовые данные успешно добавлены в базу данных."))