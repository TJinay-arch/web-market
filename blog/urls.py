from django.urls import path

from .views import (MyRecordsListView, PublishRecordView, RecordCreateView,
                    RecordDeleteView, RecordDetailView, RecordListView,
                    RecordUpdateView)

app_name = "blog"

urlpatterns = [
    path("blogs/", RecordListView.as_view(), name="record-list"),
    path("blogs/create/", RecordCreateView.as_view(), name="record-create"),
    path("blogs/<int:pk>/", RecordDetailView.as_view(), name="record-detail"),
    path("blogs/<int:pk>/update/", RecordUpdateView.as_view(), name="record-update"),
    path("blogs/<int:pk>/delete/", RecordDeleteView.as_view(), name="record-delete"),
    path("blogs/records/", MyRecordsListView.as_view(), name="my-records-view"),
    path("blogs/<int:pk>/publish/", PublishRecordView.as_view(), name="record-publish"),
]
