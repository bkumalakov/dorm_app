from django.contrib import admin
from django.contrib.auth.models import Group
from .models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.


class UsersAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_admin', 'is_verified', 'phone_number', 'first_name', 'last_name', 'patronymic',
                    'date_joined', 'last_login', )
    search_fields = ('username', 'first_name', 'last_name',)
    readonly_fields = ('id', 'password', 'is_active', 'is_staff', 'status', 'is_admin', 'is_superuser', 'date_joined',
                       'last_login')
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )


admin.site.register(Users, UsersAdmin)


