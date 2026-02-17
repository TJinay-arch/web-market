from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from catalog.models import Product


class Command(BaseCommand):
    help = "Создает группу 'Модератор продуктов' с необходимыми правами."

    def handle(self, *args, **options):
        # Получаем или создаем группу
        group, created = Group.objects.get_or_create(name="Модератор продуктов")

        if created:
            self.stdout.write(self.style.SUCCESS(f"Группа '{group.name}' успешно создана."))
        else:
            self.stdout.write(self.style.WARNING(f"Группа '{group.name}' уже существует."))

        # Получаем ContentType для модели Product
        content_type = ContentType.objects.get_for_model(Product)

        # Получаем права
        permissions_to_add = []

        # Кастомное право can_unpublish_product
        try:
            unpublish_permission = Permission.objects.get(
                codename="can_unpublish_product",
                content_type=content_type
            )
            permissions_to_add.append(unpublish_permission)
            self.stdout.write("Право 'can_unpublish_product' найдено.")
        except Permission.DoesNotExist:
            self.stdout.write(
                self.style.ERROR("Право 'can_unpublish_product' не найдено. Убедитесь, что миграции применены."))

        # Право на удаление продукта
        try:
            delete_permission = Permission.objects.get(
                codename="delete_product",
                content_type=content_type
            )
            permissions_to_add.append(delete_permission)
            self.stdout.write("Право 'delete_product' найдено.")
        except Permission.DoesNotExist:
            self.stdout.write(self.style.ERROR("Право 'delete_product' не найдено."))

        # Добавляем права к группе
        if permissions_to_add:
            group.permissions.add(*permissions_to_add)
            self.stdout.write(self.style.SUCCESS(f"Права успешно добавлены к группе '{group.name}'."))
        else:
            self.stdout.write(self.style.WARNING("Не найдено прав для добавления."))

        self.stdout.write(self.style.SUCCESS("Команда выполнена успешно."))
