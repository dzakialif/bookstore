from django import template

register = template.Library()  # Digunakan untuk mendaftarkan custom tags/filters


@register.filter(name='has_group')
def has_group(user, group_name):
    """
    Check if a user belongs to a specific group.
    """
    return user.groups.filter(name=group_name).exists()
