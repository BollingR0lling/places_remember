from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import login, home, add_memory, delete_memory

urlpatterns = [
    path('', login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('social_auth/', include('social_django.urls', namespace='social')),
    path('home', home, name='home'),
    path('add_memory', add_memory, name='add_memory'),
    path('delete_memory/<str:memory_id>', delete_memory, name='delete_memory')
]
