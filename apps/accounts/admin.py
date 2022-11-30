from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from . import models


@admin.register(models.User)
class UserAdmin(UserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active")
    search_fields = ("username", "first_name", "last_name", "email")
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("picture",)}),)
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("picture",)}),)


# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)
