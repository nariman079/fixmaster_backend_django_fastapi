from django.contrib import admin

from ..models.organization_models import (Booking, Business, CollectionImages, Customer, Image,
                     Master, Order, Service)

admin.site.register(Image)
admin.site.register(CollectionImages)
admin.site.register(Business)
admin.site.register(Master)
admin.site.register(Service)
admin.site.register(Customer)
admin.site.register(Booking)
admin.site.register(Order)

admin.site.site_header = 'Административная панель (FixMaster)'                    # default: "Django Administration"
admin.site.index_title = 'Сервис для удобного бронирования'                 # default: "Site administration"
admin.site.site_title = 'Сервис для удобного бронирования'