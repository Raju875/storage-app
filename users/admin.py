from django.contrib.sessions.models import Session
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from .models import Feedback
from users.forms import UserChangeForm, UserCreationForm
from modules.utils import *

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (("User", {"fields": ("name",)}),) + auth_admin.UserAdmin.fieldsets
    list_display = ["username", "name", "is_superuser"]
    search_fields = ["username", "name"]
    list_per_page = 25


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'description', 'is_active')
    list_display = ["user", "email", "short_description"]
    search_fields = ["user__username"]
    list_per_page = 25


    def email(self, obj):
        return obj.user.email


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['session_key', '_session_data', 'expire_date']
    readonly_fields = ('_session_data',)
    exclude = ['session_data']
    list_per_page = 25

    def _session_data(self, obj):
        return json_style_prettify(obj.get_decoded())
