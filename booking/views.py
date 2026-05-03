from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import BookingForm
from .models import Booking

def booking_create(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.client = request.user
            booking.save()
            return redirect('booking_success')
    else:
        form = BookingForm()
    return render(request, 'booking/create.html', {'form': form})

def booking_success(request):
    return render(request, 'booking/success.html')

@login_required  # Без входа — редирект на логин
def account(request):
    bookings = Booking.objects.filter(
        client=request.user
    ).order_by('-created_at')  # Сначала новые
    return render(request, 'booking/account.html', {'bookings': bookings})
