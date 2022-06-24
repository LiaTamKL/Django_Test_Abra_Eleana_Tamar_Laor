from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class AccountAdmin(UserAdmin):
    def has_add_permission(self, request, obj=None):
         return False
    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin')# 'is_customer', 'is_airline')
    search_fields = ('email', 'username', 'date_joined', 'is_admin')
    readonly_fields = ['date_joined', 'last_login', 'email', 'username']

    filter_horizontal =()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, AccountAdmin)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['by_user', 'to_user','creation_data', 'read', 'link']
    list_display_links = ('link',)