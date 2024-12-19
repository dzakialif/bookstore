from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    UserChangeForm,
    SetPasswordForm,
)
from django.contrib.auth.models import User
from .models import Profile
from .validators import *

from django import forms
from django.forms.widgets import TextInput, PasswordInput


class UserInfoForm(forms.ModelForm):
    phone = forms.CharField(
        required=False,
        validators=[validate_phone],  # Validasi nomor telepon
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Phone Number...',
        })
    )
    address = forms.CharField(
        required=False,
        validators=[validate_address],  # Validasi alamat
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter address...',
        })
    )
    city = forms.CharField(
        required=False,  # Validasi nomor telepon
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter City...',
        })
    )
    zipcode = forms.CharField(
        required=False,
        validators=[validate_zipcode],  # Validasi kode pos
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Your zipcode...',
        })
    )
    class Meta:
        model = Profile
        fields = ('phone', 'address', 'city', 'zipcode')
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Set fields as optional
            self.fields['phone'].required = False
            self.fields['address'].required = False
            self.fields['city'].required = False
            self.fields['zipcode'].required = False
        
        

class ChangePasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        required=True,
        validators=[validate_password_strength],  # Validasi kekuatan password
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
    )
    new_password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Re-enter password'
        })
    )

class UpdateUserForm(UserChangeForm):
    password = None  # Hapus field password dari form

    email = forms.EmailField(
        required=True,
        validators=[validate_unique_email],  # Validasi email unik
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter email address'
        })
    )
    username = forms.CharField(
        required=True,
        validators=[validate_unique_username],  # Validasi username unik
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter username'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter first name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter last name'
            }),
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
        # Tambahkan validasi ke field 'username' untuk memastikan tidak ada username duplikat
        self.fields['username'].validators.append(validate_unique_username)

        # Tambahkan validasi ke field 'email' untuk memastikan tidak ada email duplikat
        self.fields['email'].validators.append(validate_unique_email)

        # Set widget dan placeholder untuk password1 dan password2
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

        # Validasi kekuatan password (password1)
        self.fields['password1'].validators.append(validate_password_strength)
        
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