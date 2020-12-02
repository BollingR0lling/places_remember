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
        widget=TextInput(attrs={"placeholder": "Memory place"}))

    title = CharField(
        label='',
        widget=TextInput(attrs={"placeholder": "Your memory"})
    )
    description = CharField(
        label='',
        widget=Textarea(attrs={
            "placeholder": "Describe your memory"
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
            raise ValidationError('This place is not exists')
