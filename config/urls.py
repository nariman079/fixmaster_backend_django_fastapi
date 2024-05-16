from django.conf import settings
from django.conf.urls.static import static

from django.urls import include, path

from src.admin import content_management_admin

urlpatterns = [
    path('admin/content-management/', content_management_admin.urls),
    path('src/', include('src.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
