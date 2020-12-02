from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from geopy.geocoders import Nominatim
from .forms import MemoryModelForm
from .models import Memory
import folium


def login(request):
    return render(request, 'login.html')


@login_required
def home(request):
    m = folium.Map(width=1250, height=750, location=[56.8334, 60.5984])
    memories = Memory.objects.filter(user=request.user)
    if memories:
        for memory in memories:
            geolocator = Nominatim(user_agent='Mozilla/5.0')
            location = geolocator.geocode(memory.location)
            folium.Marker(
                [location.latitude, location.longitude],
                popup=f'{str(memory.title.encode("unicode_escape").decode())}',
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(m)
    html_map = m._repr_html_()
    context = {
        'memories': memories,
        'map': html_map,
    }
    return render(request, 'home.html', context)


@login_required
def add_memory(request):
    form = MemoryModelForm(request.POST or None)
    m = folium.Map(width=1250, height=750, location=[56.8334, 60.5984])._repr_html_()
    if form.is_valid():
        memory = Memory.objects.create(
            user=request.user,
            location=form.cleaned_data.get('location'),
            title=form.cleaned_data.get('title'),
            description=form.cleaned_data.get('description')
        )

        memory.save()
        return redirect('home')

    context = {
        'form': form,
        'map': m,
    }
    return render(request, 'add_memory.html', context)


@login_required
def delete_memory(request, *args, **kwargs):
    memory = Memory.objects.get(title=kwargs.get('memory_title'))
    memory.delete()
    return redirect('home')
