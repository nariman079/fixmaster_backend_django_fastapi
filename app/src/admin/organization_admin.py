"""
Настройка админ панели
"""

from django.contrib import admin
from django.utils.html import format_html

from src.models import (
    Organization,
    OrganizationType,
    Image,
    Service,
    Master,
    Customer,
    Moderator,
    Booking,
    Order,
)


class ContentManagementArea(admin.AdminSite):
    """
    Customization admin panel for content management
    """

    site_header = "Управление контентом"
    site_title = "Контент сайта"


content_management_admin = ContentManagementArea(name="Content management")


class MasterServiceTabularInilne(admin.TabularInline):
    """Табличная строка услуг"""

    model = Service


class OrganizationMasterInlinel(admin.TabularInline):
    """Табличная строка мастеров"""

    model = Master


class OrganizationImageInlinel(admin.StackedInline):
    """Табличная строка фотографий"""

    model = Image

    list_display = ("image",)
    classes = ["collapse"]


# Model admins
class MasterAdmin(admin.ModelAdmin):
    """Master model admin"""

    list_display = ("name", "surname", "gender")
    list_display_links = ("name",)

    inlines = [MasterServiceTabularInilne]


class OrganizationAdmin(admin.ModelAdmin):
    """Master model admin"""

    list_display = ("title", "contact_phone", "organization_type")
    list_display_links = ("title",)
    inlines = [OrganizationMasterInlinel, OrganizationImageInlinel]


class CustomerAdmin(admin.ModelAdmin):
    """Настройка админ панели Клиента"""

    list_display = ("username", "telegram_id", "phone")
    list_display_links = ("username",)


class ImageAdmin(admin.ModelAdmin):
    """Настройка админ панели Изображений"""

    list_display = ("get_image_url", "organization", "priority")
    list_filter = ("organization",)

    def get_image_url(self, obj: Image):
        """Получение ссылки на Изображение"""
        return format_html(f'<img src="{obj.image_url}" width="300px">')


content_management_admin.register(Moderator)
content_management_admin.register(Master, MasterAdmin)
content_management_admin.register(Organization, OrganizationAdmin)
content_management_admin.register(OrganizationType)
content_management_admin.register(Customer, CustomerAdmin)
content_management_admin.register(Booking)
content_management_admin.register(Image, ImageAdmin)


class OrderModelAdmin(admin.ModelAdmin):
    """Настройка админ панели Заказов"""

    model = Order


content_management_admin.register(Order, OrderModelAdmin)
