from django.db import models


class Records(models.Model):
    name = models.CharField(max_length=150, verbose_name="Заголовок")
    description = models.TextField(blank=True, null=True, verbose_name="Содержимое")
    image = models.ImageField(upload_to="records/", blank=True, null=True, verbose_name="Превью")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_published = models.BooleanField(default=False, verbose_name="Признак публикации")
    view_count = models.IntegerField(default=0, verbose_name="Количество просмотров")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"
        ordering = ["name"]
