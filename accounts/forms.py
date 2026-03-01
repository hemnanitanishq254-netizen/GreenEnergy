from django import forms
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from .models import User, ProducerProfile, ConsumerProfile, InvestorProfile


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'role', 'phone',
                  'address', 'city', 'state', 'pincode', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='col-md-6'),
                Column('email', css_class='col-md-6'),
            ),
            Row(
                Column('first_name', css_class='col-md-6'),
                Column('last_name', css_class='col-md-6'),
            ),
            Row(
                Column('role', css_class='col-md-6'),
                Column('phone', css_class='col-md-6'),
            ),
            'address',
            Row(
                Column('city', css_class='col-md-4'),
                Column('state', css_class='col-md-4'),
                Column('pincode', css_class='col-md-4'),
            ),
            Row(
                Column('password1', css_class='col-md-6'),
                Column('password2', css_class='col-md-6'),
            ),
            Submit('submit', 'Register', css_class='btn btn-success w-100 mt-3')
        )


class ProducerProfileForm(forms.ModelForm):
    class Meta:
        model = ProducerProfile
        fields = ['energy_type', 'capacity_kw', 'installation_date', 'certification_number',
                  'certification_doc', 'latitude', 'longitude', 'description']
        widgets = {
            'installation_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class ConsumerProfileForm(forms.ModelForm):
    class Meta:
        model = ConsumerProfile
        fields = ['monthly_consumption_kwh', 'preferred_energy_type', 'budget_per_month']


class InvestorProfileForm(forms.ModelForm):
    class Meta:
        model = InvestorProfile
        fields = ['company_name', 'investment_capacity', 'pan_number', 'preferred_sectors']
        widgets = {
            'preferred_sectors': forms.Textarea(attrs={'rows': 3}),
        }