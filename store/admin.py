from django.contrib import admin
from django.contrib.auth.models import User
from .models import (
    Category,
    Product,
    Profile,
)
# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ['slug']
    
admin.site.register(Product)
admin.site.register(Profile)

# Mix profile info and user info
class ProfileInline(admin.StackedInline):
	model = Profile

# Extend User Model
class UserAdmin(admin.ModelAdmin):
	model = User
	field = ["username", "first_name", "last_name", "email"]
	inlines = [ProfileInline]

# Unregister the old way
admin.site.unregister(User)

# Re-Register the new way
admin.site.register(User, UserAdmin)