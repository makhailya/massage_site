from django.urls import path
from . import views

urlpatterns = [
    path('booking/', views.booking_create, name='booking_create'),
    path('booking/success/', views.booking_success, name='booking_success'),
    path('account/', views.account, name='account'),
]
