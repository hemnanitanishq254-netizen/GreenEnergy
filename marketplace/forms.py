from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from .models import EnergyListing


class EnergyListingForm(forms.ModelForm):
    class Meta:
        model = EnergyListing
        fields = ['title', 'quantity_kwh', 'price_per_kwh', 'available_from',
                  'available_until', 'description', 'location']
        widgets = {
            'available_from': forms.DateInput(attrs={'type': 'date'}),
            'available_until': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'title',
            Row(
                Column('quantity_kwh', css_class='col-md-6'),
                Column('price_per_kwh', css_class='col-md-6'),
            ),
            Row(
                Column('available_from', css_class='col-md-6'),
                Column('available_until', css_class='col-md-6'),
            ),
            'location',
            'description',
            Submit('submit', 'Create Listing', css_class='btn btn-success w-100 mt-3')
        )