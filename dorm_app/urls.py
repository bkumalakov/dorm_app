
from django.contrib import admin
from django.urls import path, include

admin.site.site_header = 'Система АУНиГ'
admin.site.site_title = 'Система АУНиГ'
admin.site.index_title = 'Система АУНиГ'

urlpatterns = [
    path('', include('oil_grants.urls')),
    path('admin/', admin.site.urls),
]
