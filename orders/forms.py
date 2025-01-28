from django import forms
from orders.models import Customer

class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    phone = forms.CharField(max_length=15, required=True, help_text="Enter your phone number with the country code (e.g., +1234567890)")

    class Meta:
        model = Customer
        fields = ['name', 'password', 'phone']
