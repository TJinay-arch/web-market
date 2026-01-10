from django.forms import ModelForm

from .models import Records


class RecordForm(ModelForm):
    class Meta:
        model = Records
        fields = ["name", "description", "image"]
