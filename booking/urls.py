from django.urls import path
from . import views

urlpatterns = [
    path('booking/', views.booking_create, name='booking_create'),
    path('booking/success/', views.booking_success, name='booking_success'),
    path('account/', views.account, name='account'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/update/<int:booking_id>/', views.booking_update_status, name='booking_update_status'),
]