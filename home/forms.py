from django import forms 
from .models import Request, CalculatePriceRequest


class FeedbackForm(forms.ModelForm): 
    class Meta:
        model = Request
        fields = ['name', 'phone', 'message']
        labels = {
            'name': 'Имя',
            'phone': 'Телефон',
            'message': 'Сообщение'
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Имя *',
            }),
            'phone': forms.TextInput(attrs={
                'type': 'tel', 
                'placeholder': 'Телефон *',
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Сообщение',
                'rows': 5,
            })
        }


class CalculatePriceRequestForm(forms.ModelForm):
    class Meta:
        model = CalculatePriceRequest
        fields = ['city', 'phone', 'message', 'container_type', 'service_type']
        labels = {
            'city': 'Город',
            'phone': 'Телефон',
            'message': 'Сообщение'
        }
        widgets = {
            'city': forms.TextInput(attrs={
                'placeholder': 'Город *',
            }),
            'phone': forms.TextInput(attrs={
                'type': 'tel', 
                'placeholder': 'Телефон *',
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Сообщение',
                'rows': 5,
            })
        }