from django.contrib import admin

from .models import Subscription, User


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'username', 'first_name', 'last_name')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    list_filter = ('email', 'username', 'first_name', 'last_name')


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'author',)


admin.site.register(User, UserAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
