from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  RedirectView, UpdateView)

from .forms import RecordForm
from .models import Records


class RecordCreateView(CreateView):
    model = Records
    form_class = RecordForm
    template_name = "blog/create.html"
    success_url = reverse_lazy("blog:record-list")

    def form_valid(self, form):
        obj = form.save(commit=False)

        if self.request.POST.get("save_as_draft"):
            obj.is_published = False
        else:
            obj.is_published = True

        obj.save()

        return super().form_valid(form)


class RecordDetailView(DetailView):
    model = Records
    template_name = "blog/detail_blog.html"
    context_object_name = "record"

    def get_object(self, queryset=None):
        record = super().get_object(queryset=queryset)
        record.view_count += 1
        record.save(update_fields=["view_count"])
        return record


class RecordUpdateView(UpdateView):
    model = Records
    form_class = RecordForm
    template_name = "blog/update.html"
    success_url = reverse_lazy("blog:record-list")


class RecordDeleteView(DeleteView):
    model = Records
    template_name = "blog/delete_record.html"
    success_url = reverse_lazy("blog:record-list")


class RecordListView(ListView):
    model = Records
    template_name = "blog/list_records.html"
    context_object_name = "records"
    paginate_by = 10

    def get_queryset(self):
        return Records.objects.order_by("-created_at")


class MyRecordsListView(ListView):
    model = Records
    template_name = "blog/my_records.html"
    context_object_name = "records"
    paginate_by = 10

    def get_queryset(self):
        # Возвращаем ВСЕ записи, включая черновики и опубликованные статьи
        return Records.objects.all().order_by("-created_at")


class PublishRecordView(RedirectView):
    permanent = False
    pattern_name = "blog:record-detail"

    def get_redirect_url(self, *args, **kwargs):
        record = get_object_or_404(Records, pk=self.kwargs["pk"])

        # Проверяем, что статья ещё не опубликована
        if not record.is_published:
            # Меняем статус публикации на True
            record.is_published = True
            record.save()

        # Возвращаем URL, куда направится пользователь после публикации
        return super().get_redirect_url(*args, **kwargs)
