from django import forms 
from .models import Request, CalculatePriceRequest, CargoTransportationRequest


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


class CargoTransportationForm(forms.ModelForm):
    class Meta:
        model = CargoTransportationRequest
        fields = ['name', 'phone', 'email', 'message', 'inn']
        labels = {
            'name': 'Имя *',
            'phone': 'Телефон *',
            'message': 'Сообщение *', 
            'email': 'E-mail', 
            'inn': 'ИНН',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Имя *',
            }),
            'phone': forms.TextInput(attrs={
                'type': 'tel', 
                'placeholder': 'Телефон *',
            }),
            'email': forms.TextInput(attrs={
                'type': 'email', 
                'placeholder': 'E-mail *',
            }),
            'inn': forms.TextInput(attrs={
                'placeholder': 'ИНН',
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Сообщение *',
                'rows': 5,
            })
        }