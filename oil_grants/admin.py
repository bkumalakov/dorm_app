from django.contrib import admin
from .models import *


class ProgramGroupAdmin(admin.ModelAdmin):
    list_display = ('g_code', 'g_name')
    search_fields = ('g_code', 'g_name')
    list_display_links = ('g_code', 'g_name',)
    readonly_fields = ('id', 'date_of_add', 'date_of_update', )
    ordering = ('-date_of_update',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class EdProgramAdmin(admin.ModelAdmin):
    list_display = ('p_code', 'p_name')
    search_fields = ('p_code', 'p_name')
    list_display_links = ('p_code', 'p_code',)
    readonly_fields = ('id', 'date_of_add', 'date_of_update', )
    ordering = ('-date_of_update',)
    filter_horizontal = ()
    list_filter = ('group', )
    autocomplete_fields = ('group', )
    fieldsets = ()


class OilCompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')
    search_fields = ('name', 'address')
    ordering = ('-date_of_update',)


class GrantAdmin(admin.ModelAdmin):
    list_display = ('oilCompany', 'student', 'date')
    search_fields = ('oilCompany__name', 'student__last_name', 'fee', 'contractNo')
    list_display_links = ('oilCompany', 'student',)
    readonly_fields = ('id', 'date_of_add', 'date_of_update', )
    ordering = ('-date_of_update',)
    filter_horizontal = ()
    list_filter = ('oilCompany', )
    autocomplete_fields = ('oilCompany', 'student')
    fieldsets = ()


class RatingAdmin(admin.ModelAdmin):
    list_display = ( 'id', 'student', 'essay', 'computerTest', 'ratingDate')
    list_editable = ('essay', 'computerTest')
    list_display_links = ('student', 'id',)
    search_fields = ('student__first_name', 'id',)
    readonly_fields = ('id', 'date_of_add', 'date_of_update', )
    autocomplete_fields = ['student', ]
    ordering = ('-date_of_update',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class CompetitionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'company', 'start', 'end', 'date_of_add', 'date_of_update', )
    list_display_links = ('company', 'status', 'id',)
    search_fields = ('company__name', 'id', 'status',)
    readonly_fields = ('id', 'date_of_add', 'date_of_update', )
    autocomplete_fields = ['company', ]
    ordering = ('-date_of_update',)
    filter_horizontal = ()
    list_filter = ('status', 'company')
    fieldsets = ()


class ParticipantsAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'is_passed', 'competition', 'date_of_add', 'date_of_update', )
    list_display_links = ('student', 'is_passed', 'id',)
    search_fields = ('student__first_name', 'student__last_name', 'id', 'competition__company__name',)
    readonly_fields = ('id', 'date_of_add', 'date_of_update', )
    ordering = ('-date_of_update',)
    filter_horizontal = ()
    autocomplete_fields = ['student', 'competition']
    list_filter = ('student', 'is_passed', 'competition')
    fieldsets = ()


admin.site.register(Participants, ParticipantsAdmin)
admin.site.register(Competitions, CompetitionsAdmin)
admin.site.register(ProgramGroup, ProgramGroupAdmin)
admin.site.register(EdProgram, EdProgramAdmin)
admin.site.register(OilCompany, OilCompanyAdmin)
admin.site.register(Grant, GrantAdmin)
admin.site.register(Rating, RatingAdmin)

