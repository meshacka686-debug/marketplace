from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "role",
        "phone",
        "verified",
    )

    list_filter = (
        "role",
        "verified",
    )

    search_fields = (
        "user__username",
        "phone",
        "shop_name",
    )