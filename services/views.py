from django.shortcuts import render
from .models import Service

def home(request):
    return render(request, 'home.html')

def service_list(request):
    services = Service.objects.filter(is_active=True)
    return render(request, 'services/list.html', {'services': services})