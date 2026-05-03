from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('services.urls')),
    path('', include('booking.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # вход/выход
    path('accounts/', include('users.urls')),  # регистрация
]