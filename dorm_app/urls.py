
from django.contrib import admin
from django.urls import path, include

admin.site.site_header = 'Общежития АУНиГ'
admin.site.site_title = 'Общежития АУНиГ'
admin.site.index_title = 'Система управления заселением в общежития АУНиГ'

urlpatterns = [
    path('', include('residents_app.urls')),
    path('admin/', admin.site.urls),
]
