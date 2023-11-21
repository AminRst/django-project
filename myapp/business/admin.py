from django.contrib import admin
from django_jalali.admin.filters import JDateFieldListFilter
from nested_admin.nested import NestedModelAdmin, NestedStackedInline, NestedTabularInline
from django.utils.translation import ngettext
from django.contrib import messages
from .models import *
from django.contrib.admin.apps import AdminConfig


# Register your models here.

@admin.register(Cafe)
class CafeAdmin(admin.ModelAdmin):
    list_display = ['name', 'manager', 'publish', 'status', 'city', 'refresh']
    ordering = ['name', 'publish']
    list_filter = ['status', 'address', 'manager']
    search_fields = ['name', 'description']
    raw_id_fields = ['manager']
    date_hierarchy = 'publish'
    prepopulated_fields = {"slug": ['name']}
    list_editable = ['status', 'city', 'refresh']
    actions = ['make_open', 'make_close', 'refresh']

    @admin.action(description='باز کردن کافه های انتخاب شده')
    def make_open(self, request, queryset):
        updated = queryset.update(status="OP")
        self.message_user(
            request,
            ngettext(
                "%d کافه با موفقیت باز شد.",
                "%d کافه  با موفقیت باز شدند.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )

    @admin.action(description='بستن  کافه های انتخاب شده')
    def make_close(self, request, queryset):
        updated = queryset.update(status="CL")
        self.message_user(
            request,
            ngettext(
                "%d کافه با موفقیت بسته شد.",
                "%d کافه با موفقیت بسته شدند.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )

    @admin.action(description='last cafes refresh')
    def refresh(self, request, queryset):
        refresh = queryset.update(refresh=True)
        self.message_user(
            request,
            ngettext(
                "%d کافه با موفقیت تازه سازی شد.",
                "%d کافه ها با موفقیت تازه سازی شدند.",
                refresh,
            )
            % refresh,
            messages.SUCCESS,
        )

    def get_likes(self, obj):
        return [likes.name for likes in obj.likes.all()]


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'phone']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['cafe', 'name', 'created', 'active', 'body']
    list_filter = ['active', ('created', JDateFieldListFilter)]
    search_fields = ['name', 'body']
    list_editable = ['active']


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'message']
    list_filter = ['name', 'email']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['cafe', 'title', 'created']


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'bio', 'photo']


# @admin.register(Like)
# class LikeAdmin(admin.ModelAdmin):
#     list_display = ['cafe']


# @admin.register(MenuItems)
class MenuItemsAdmin(NestedTabularInline):
    model = MenuItems
    extra = 0


# @admin.register(Section)
class SectionAdmin(NestedTabularInline):
    model = Section
    extra = 0
    inlines = [MenuItemsAdmin, ]


# @admin.register(Menu)
class MenuAdmin(NestedModelAdmin):
    inlines = [SectionAdmin, ]


admin.site.register(Menu, MenuAdmin)


class MyAdminConfig(AdminConfig):
    default_site = "admin_reorder.ReorderingAdminSite"
