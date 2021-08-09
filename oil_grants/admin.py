from django.contrib import admin
from . import models


class ProgramGroupAdmin(admin.ModelAdmin):
    list_display = ('g_code', 'g_name')
    search_fields = ('g_code', 'g_name')


class EdProgramAdmin(admin.ModelAdmin):
    list_display = ('p_code', 'p_name')
    search_fields = ('p_code', 'p_name')


class OilCompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')


class GrantAdmin(admin.ModelAdmin):
    list_display = ('oilCompany', 'student', 'date')


class RatingAdmin(admin.ModelAdmin):
    list_display = ('student', 'essay', 'computerTest', 'ratingDate')
    list_editable = ('essay', 'computerTest')


admin.site.register(models.ProgramGroup, ProgramGroupAdmin)
admin.site.register(models.EdProgram, EdProgramAdmin)
admin.site.register(models.OilCompany, OilCompanyAdmin)
admin.site.register(models.Grant, GrantAdmin)
admin.site.register(models.Rating, RatingAdmin)

