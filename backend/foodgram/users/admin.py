from django.contrib import admin

from .models import Subscription, User


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'username',)
    search_fields = ('email', 'username',)
    list_filter = ('email', 'username',)


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'author',)


admin.site.register(User)
admin.site.register(Subscription)
