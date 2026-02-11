"""
SmartSolutions VE - URLs principales
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "SmartSolutions VE"
admin.site.site_title = "SmartSolutions Admin"
admin.site.index_title = "Panel de Administración"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.landing.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
