from django import forms
from .models import ShippingAddress, PaymentInfo
from django.core.exceptions import ValidationError
import re
from datetime import datetime

class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = [
            'shipping_full_name',
            'shipping_email',
            'shipping_address',
            'shipping_city',
            'shipping_zipcode',
        ]
        exclude = ['user',]
            
        widgets = {
            'shipping_full_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter Full Name...',
                }
            ),
            'shipping_email': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter Email...',
                }
            ),
            'shipping_address': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter Address...',
                }
            ),
            'shipping_city': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter City...',
                }
            ),
            'shipping_zipcode': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter Zipcode...',
                }
            ),
        }
    def __init__(self, *args, require_all_fields=False, **kwargs):
        super().__init__(*args, **kwargs)
        # Set required property dynamically
        for field_name in self.fields:
            self.fields[field_name].required = require_all_fields
        

class PaymentForm(forms.ModelForm):
    class Meta:
        model = PaymentInfo
        fields = ['card_name', 'card_number', 'card_cvv_number']
        
    card_name = forms.CharField(
        label="", 
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Name On Card'}), 
        required=True
    )
    card_number = forms.CharField(
        label="", 
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Card Number'}),
        required=True
    )
    card_cvv_number = forms.CharField(
        label="", 
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'CVV Code'}),
        required=True
    )

    # Custom validation for card number
    def clean_card_number(self):
        card_number = self.cleaned_data.get('card_number')
        if not re.match(r"^\d{16}$", card_number):
            raise ValidationError("Card number must be exactly 16 digits.")
        return card_number

    # Custom validation for CVV
    def clean_card_cvv_number(self):
        card_cvv = self.cleaned_data.get('card_cvv_number')
        if not re.match(r"^\d{3,4}$", card_cvv):
            raise ValidationError("CVV must be 3 or 4 digits.")
        return card_cvv
