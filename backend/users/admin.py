from django.contrib import admin
from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from .models import Subscription

User = get_user_model()


class FoodgramUserAdmin(UserAdmin):
    list_display = ['email', 'username', ]
    list_filter = ['email', 'username', ]


@register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    autocomplete_fields = ('author', 'user')


admin.site.unregister(User)
admin.site.register(User, FoodgramUserAdmin)
