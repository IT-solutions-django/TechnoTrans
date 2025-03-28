from django import forms
from .models import (
    Generator, 
    GeneratorPower, 
    GeneratorType, 
    GeneratorCategory,
)


class GeneratorFilterForm(forms.Form):
    price = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    year = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    container_type = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    brand = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    category = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    generator_type = forms.MultipleChoiceField(
        required=False, 
        widget=forms.CheckboxSelectMultiple
    )
    power = forms.MultipleChoiceField(
        required=False, 
        widget=forms.CheckboxSelectMultiple
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['price'].choices = [
            ('500000-1000000', 'От 500 тыс. до 1 млн. руб'),
            ('1000000-3000000', 'От 1 млн. до 3 млн. руб'),
            ('3000000-', 'Свыше 3 млн. руб')
        ]

        self.fields['year'].choices = [
            (y, y) for y in sorted(
                set(Generator.objects.values_list('year', flat=True)), reverse=True
            )
        ]

        self.fields['category'].choices = GeneratorCategory.objects.values_list('id', 'name')
        self.fields['power'].choices = GeneratorPower.objects.values_list('id', 'name')
        self.fields['generator_type'].choices = GeneratorType.objects.values_list('id', 'name')