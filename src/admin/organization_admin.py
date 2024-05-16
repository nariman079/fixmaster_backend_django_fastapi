"""
Setting up admin panels
"""
from django.contrib import admin
from django.utils.html import format_html

from src.models import Organization, OrganizationType, Image, Service, Master

class ContentManagementArea(admin.AdminSite):
    """
    Customization admin panel for content management
    """
    site_header = "Управление контентом"
    site_title = "Контент сайта"

content_management_admin = ContentManagementArea(name="Content management")


class MasterServiceTabularInilne(admin.TabularInline):
    model = Service


class MasterAdmin(admin.ModelAdmin):
    """ Master model admin """
    list_display = ('avatar', 'name', 'surname', 'gender')

    inlines = [
        MasterServiceTabularInilne
    ]

    def avatar(self,obj: Master):
        """
        Generating image for the admin panel of the wizard 
        """
        print(obj.image.__dict__)
        return format_html(f"""<img src="{obj.image} width="100px">""")

content_management_admin.register(Master, MasterAdmin)

content_management_admin.register(
    [Organization,
    OrganizationType,
    Image,
    Service]
)