from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

admin.site.site_header = 'Система АУНиГ'
admin.site.site_title = 'Система АУНиГ'
admin.site.index_title = 'Система АУНиГ'

urlpatterns = [
    path('', include('oil_grants.urls')),
    path('users/', include('users_app.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
