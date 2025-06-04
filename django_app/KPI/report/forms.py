from django import forms
from .models import KpiDetails, Kpi
import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class KpiForm(forms.ModelForm):

    KPI_CHOICES = [
        ('Conducting PAT', 'Conducting PAT'),
        ('profit', 'Profit'),
        ('customer_satisfaction', 'Customer Satisfaction'),
        # Add more choices
    ]

    kpi = forms.ChoiceField(choices=KPI_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Kpi
        fields = [
            'weeks',
            'activity',
            'kpi',
            'baseline',
            'plan',

        ]
        widgets = {
            'activity': forms.TextInput(attrs={'class': 'form-control'}),
            'baseline': forms.NumberInput(attrs={'class': 'form-control'}),
            'plan': forms.NumberInput(attrs={'class': 'form-control'}),
            'weeks': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class KpiDetailsForm(forms.ModelForm):
    class Meta:
        model = KpiDetails
        fields = ['kpi', 'progress']
        widgets = {
            'kpi': forms.Select(attrs={'class': 'form-control'}),
            'progress': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter progress'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(KpiDetailsForm, self).__init__(*args, **kwargs)

        if user is not None:
            # Get all KPIs by this user
            user_kpis = Kpi.objects.filter(created_by=user)

            # Get IDs of KPIs that already have progress submitted
            submitted_kpi_ids = KpiDetails.objects.values_list('kpi_id', flat=True)

            # Filter to only show unsubmitted KPIs
            self.fields['kpi'].queryset = user_kpis.exclude(id__in=submitted_kpi_ids)