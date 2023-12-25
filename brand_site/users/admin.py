from django.contrib import admin
from .models import NewUser, Profile
from django.contrib.auth.admin import UserAdmin
from django.forms import Textarea


class UserAdminConfig(UserAdmin):
    model = NewUser
    search_fields = ('phone', 'email',)
    list_filter = ('phone', 'email', 'first_name', 'is_superuser', 'is_staff')
    ordering = ('-start_date',)
    list_display = ('phone', 'email', 'first_name',
                    'is_superuser', 'is_staff')
    fieldsets = (
        (None, {'fields': ('phone','email')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'email', 'first_name', 'password1', 'password2', 'is_superuser', 'is_staff')}
         ),
    )

admin.site.register(NewUser)
admin.site.register(Profile)
