import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Validasi untuk nomor telepon
def validate_phone(value):
    phone_regex = r'^\+?[\d\s]{10,15}$'
    if not re.match(phone_regex, value):
        raise ValidationError('Phone number must be in a valid format (e.g., +1234567890 or 123 456 7890).')
    if len(value) < 11:
        raise ValidationError(_('Phone number should be at least 11 digits long.'))

# Validasi untuk kode pos
def validate_zipcode(value):
    if not value.isdigit() or len(value) != 5:
        raise ValidationError(_('Invalid zipcode format. It should be a 5-digit number.'))

# Validasi untuk alamat (minimal panjang alamat)
def validate_address(value):
    if len(value) < 10:
        raise ValidationError(_('Address should be at least 10 characters long.'))

# Validasi untuk password
def validate_password_strength(value):
    if len(value) < 8:
        raise ValidationError(_('Password must be at least 8 characters long.'))
    if not any(char.isdigit() for char in value):
        raise ValidationError(_('Password must contain at least one digit.'))

# Validasi untuk email (untuk memastikan email tidak duplikat)
def validate_unique_email(value):
    from django.contrib.auth.models import User
    if User.objects.filter(email=value).exists():
        raise ValidationError(_('This email address is already registered.'))

# Validasi untuk username (untuk memastikan username tidak duplikat)
def validate_unique_username(value):
    from django.contrib.auth.models import User
    if User.objects.filter(username=value).exists():
        raise ValidationError(_('This username is already taken.'))
