from django.forms import (
    ModelForm,
    CharField,
    Textarea,
    TextInput,
    ValidationError
)
from geopy import Nominatim
from .models import Memory


class MemoryModelForm(ModelForm):
    location = CharField(
        label='',
        widget=TextInput(attrs={"placeholder": "Место воспоминания"}))

    title = CharField(
        label='',
        widget=TextInput(attrs={"placeholder": "Придумайте для него название"})
    )
    description = CharField(
        label='',
        widget=Textarea(attrs={
            "placeholder": "Опишите его"
        })
    )

    class Meta:
        model = Memory
        fields = ('location', 'title', 'description')

    def clean_location(self, *args, **kwargs):
        location = self.cleaned_data.get('location')
        geolocator = Nominatim(user_agent='Mozilla/5.0')
        try:
            place = geolocator.geocode(location)
            p_lat, p_lon = place.latitude, place.longitude
            return location
        except AttributeError:
            raise ValidationError('Такого места нет на карте, проверьте ввод')
