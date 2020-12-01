from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import MemoryModelForm
from .models import Memory
import folium


def login(request):
    return render(request, 'login.html')


@login_required
def home(request):
    context = {
        'memories': Memory.objects.filter(user=request.user),
    }
    return render(request, 'home.html', context)


@login_required
def add_memory(request):
    form = MemoryModelForm(request.POST or None)
    m = folium.Map(width=1250, height=750)._repr_html_()

    if form.is_valid():
        memory = Memory.objects.create(
            user=request.user,
            location=form.cleaned_data.get('location'),
            title=form.cleaned_data.get('title'),
            description=form.cleaned_data.get('description')
        )
        memory.save()
        return home(request)

    context = {
        'form': form,
        'map': m,
    }
    return render(request, 'add_memory.html', context)
