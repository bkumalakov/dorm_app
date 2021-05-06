from django.contrib import admin
from . import models


class DormAdmin(admin.ModelAdmin):
    list_display = ('d_name', 'capacity')


class RoomAdmin(admin.ModelAdmin):
    list_display = ('r_number', 'r_floor', 'r_type', 'dorm_id')
    list_filter = ('r_type', 'dorm_id')


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('t_name', 't_surname', 't_sex', 't_type')
    list_filter = ('t_sex', 't_type')


admin.site.register(models.Dorm, DormAdmin)
admin.site.register(models.Room, RoomAdmin)
admin.site.register(models.Application, ApplicationAdmin)
admin.site.register(models.Registration)
