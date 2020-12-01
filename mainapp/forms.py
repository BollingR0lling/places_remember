from django.forms import ModelForm
from .models import Memory


class MemoryModelForm(ModelForm):
    class Meta:
        model = Memory
        fields = ('location', 'title', 'description')
