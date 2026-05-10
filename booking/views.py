from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .forms import BookingForm
from .models import Booking

def booking_create(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect(f'{settings.LOGIN_URL}?next={request.path}')
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

@login_required(login_url='/accounts/login/')  # Требует обычный вход, редирект на пользовательский login
def dashboard(request):
    bookings = Booking.objects.select_related('client', 'service').order_by('-created_at')
    context = {
        'bookings': bookings,
        'total_bookings': bookings.count(),
        'pending_bookings': bookings.filter(status='pending').count(),
        'client_count': bookings.values('client').distinct().count(),
    }
    return render(request, 'booking/dashboard.html', context)


def booking_update_status(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        allowed_statuses = {choice[0] for choice in Booking.STATUS_CHOICES}
        if status in allowed_statuses:
            booking.status = status
            booking.save(update_fields=['status'])
    return redirect('dashboard')
