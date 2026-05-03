from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['service', 'date', 'time', 'comment']
        widgets = {
            'date': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            ),
            'time': forms.TimeInput(
                attrs={'type': 'time'}
            ),
            'comment': forms.Textarea(
                attrs={'rows': 3, 'placeholder': 'Пожелания или вопросы...'}
            ),
        }
