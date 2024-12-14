from django import forms
from .models import ShippingAddress

class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = [
            'shipping_full_name',
            'shipping_email',
            'shipping_address1',
            'shipping_address2',
            'shipping_city',
            'shipping_zipcode',
        ]
        exclude = ['user',]
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Set fields as optional
            self.fields['shipping_full_name'].required = True
            self.fields['shipping_email'].required = True
            self.fields['shipping_address1'].required = True
            self.fields['shipping_address2'].required = False
            self.fields['shipping_city'].required = True
            self.fields['shipping_zipcode'].required = True
            
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
            'shipping_address1': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter Address...',
                }
            ),
            'shipping_address2': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Another Address...',
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
        
class PaymentForm(forms.Form):
	card_name =  forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Name On Card'}), required=True)
	card_number =  forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Card Number'}), required=True)
	card_exp_date =  forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Expiration Date'}), required=True)
	card_cvv_number =  forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'CVV Code'}), required=True)
	card_address1 =  forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Billing Address 1'}), required=True)
	card_address2 =  forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Billing Address 2'}), required=False)
	card_city =  forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Billing City'}), required=True)
	card_state = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Billing State'}), required=True)
	card_zipcode =  forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Billing Zipcode'}), required=True)
	card_country =  forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Billing Country'}), required=True)
