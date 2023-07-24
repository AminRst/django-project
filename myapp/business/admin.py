from django.contrib import admin
from django_jalali.admin.filters import JDateFieldListFilter
from .models import *


# Register your models here.
@admin.register(Cafe)
class CafeAdmin(admin.ModelAdmin):
    list_display = ['name', 'manager', 'publish', 'status']
    ordering = ['name', 'publish']
    list_filter = ['status', 'address', 'manager']
    search_fields = ['name', 'description']
    raw_id_fields = ['manager']
    date_hierarchy = 'publish'
    prepopulated_fields = {"slug": ['name']}
    list_editable = ['status']


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'phone']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['cafe', 'name', 'created', 'active']
    list_filter = ['active', ('created', JDateFieldListFilter), ('update', JDateFieldListFilter)]
    search_fields = ['name', 'body']
    list_editable = ['active']




















