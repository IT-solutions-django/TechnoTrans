from django import forms
from .models import ( 
    RepairPartCategory, 
    RepairPart, 
)
from containers.models import Brand


class RepairPartFilterForm(forms.Form):
    category = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    brand = forms.MultipleChoiceField(
        required=False, 
        widget=forms.CheckboxSelectMultiple
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['category'].choices = RepairPartCategory.objects.values_list('id', 'name')
        self.fields['brand'].choices = Brand.objects.values_list('id', 'name')
