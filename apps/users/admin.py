from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from imagekit.admin import AdminThumbnail

from ..core.admin import BaseAdmin
from .models import Person, User


@admin.register(User)
class UserAdmin(BaseAdmin, DjangoUserAdmin):
    """UI for User model."""

    ordering = ("email",)
    avatar_thumbnail = AdminThumbnail(image_field="avatar_thumbnail")
    list_display = (
        "avatar_thumbnail",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_superuser",
    )
    list_display_links = (
        "email",
    )
    search_fields = (
        "first_name",
        "last_name",
        "email",
    )
    add_fieldsets = (
        (
            None, {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    fieldsets = (
        (
            None, {
                "fields": (
                    "email",
                    "password",
                ),
            },
        ),
        (
            _("Personal info"), {
                "fields": (
                    "first_name",
                    "last_name",
                    "avatar",
                ),
            },
        ),
        (
            _("Permissions"), {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )


@admin.register(Person)
class PersonAdmin(BaseAdmin):
    """UI for Person model."""

    list_display = (
        "first_name",
        "last_name",
        "birth_date",
    )
    search_fields = (
        "first_name",
        "last_name",
    )
    date_hierarchy = "birth_date"
    fieldsets = (
        (
            None, {
                "fields": (
                    "first_name",
                    "last_name",
                    "birth_date",
                ),
            },
        ),
    )
