"""
Setting up admin panels
"""
from django.contrib import admin
from django.utils.html import format_html

from src.models import Organization, OrganizationType, Image, Service, Master, Customer, Moderator


class ContentManagementArea(admin.AdminSite):
    """
    Customization admin panel for content management
    """
    site_header = "Управление контентом"
    site_title = "Контент сайта"


content_management_admin = ContentManagementArea(name="Content management")


# Tabular inlines
class MasterServiceTabularInilne(admin.TabularInline):
    model = Service


class OrganizationMasterInlinel(admin.TabularInline):
    model = Master


class OrganizationImageInlinel(admin.TabularInline):
    model = Image


# Model admins
class MasterAdmin(admin.ModelAdmin):
    """ Master model admin """
    list_display = ('name', 'surname', 'gender')
    list_display_links = ('name',)

    inlines = [
        MasterServiceTabularInilne
    ]

class OrganizationAdmin(admin.ModelAdmin):
    """ Master model admin """
    list_display = ('title', 'contact_phone', 'organization_type')
    list_display_links = ('title',)
    inlines = [
        OrganizationMasterInlinel,
        OrganizationImageInlinel
    ]


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('username', 'telegram_id', 'phone')
    list_display_links = ('username',)


content_management_admin.register(Moderator)
content_management_admin.register(Master, MasterAdmin)
content_management_admin.register(Organization, OrganizationAdmin)
content_management_admin.register(OrganizationType)
content_management_admin.register(Customer, CustomerAdmin)