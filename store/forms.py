from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    UserChangeForm,
    SetPasswordForm,
)
from django.contrib.auth.models import User
from .models import Profile

from django import forms
from django.forms.widgets import TextInput, PasswordInput


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', 'address1', 'address2', 'city', 'zipcode')
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Set fields as optional
            self.fields['phone'].required = False
            self.fields['address1'].required = False
            self.fields['address2'].required = False
            self.fields['city'].required = False
            self.fields['zipcode'].required = False
        
        widgets = {
            'phone': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Phone Number...',
                }
            ),
            'address1': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'First address...',
                }
            ),
            'address2': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Second address...',
                }
            ),
            'city': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter Your City...',
                }
            ),
            'zipcode': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter Your zipcode...',
                }
            ),
        }
        
        
        

class ChangePasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget = forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter password'
            }
        )
        self.fields['new_password2'].widget = forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Re-enter password'
            }
        )

class UpdateUserForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter username'
                }
            ),
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter first name'
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter last name'
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter email address'
                }
            ),
        }

class RegisterForm(UserCreationForm):    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter username'
                }
            ),
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter first name'
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter last name'
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter email address'
                }
            ),
        }
        # Menimpa widgets password1 dan password2
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter password'
            }
        )
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Re-enter password'
            }
        )
        
        # Set fields as required
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        
        
class LoginForm(AuthenticationForm):
    
    username = forms.CharField(
        widget=TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter username'
            }
        )
    )
    password = forms.CharField(
        widget=PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter password'
            }
        )
    )