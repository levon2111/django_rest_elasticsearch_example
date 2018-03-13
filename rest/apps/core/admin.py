from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from rest.apps.core.models import *


class UserAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserAdmin)
