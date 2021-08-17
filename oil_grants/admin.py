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


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')
    search_fields = ('name', 'address')
    ordering = ('-date_of_update',)


class ContractAdmin(admin.ModelAdmin):
    list_display = ('company', 'student', 'sign_date')
    search_fields = ('company__name', 'student__last_name', 'fee', 'contractNo')
    list_display_links = ('company', 'student',)
    readonly_fields = ('id', 'date_of_add', 'date_of_update', )
    ordering = ('-date_of_update',)
    filter_horizontal = ()
    list_filter = ('company', )
    autocomplete_fields = ('company', 'student')
    fieldsets = ()


class CompetitionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'company', 'start', 'end', 'date_of_add', 'date_of_update', )
    list_display_links = ('company', 'status', 'id',)
    search_fields = ('company__name', 'id', 'status', 'description')
    readonly_fields = ('id', 'date_of_add', 'date_of_update', )
    autocomplete_fields = ['company', ]
    ordering = ('-date_of_update',)
    filter_horizontal = ()
    list_filter = ('status', 'company')
    fieldsets = ()


class ApplicationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'competition', 'status', 'essay', 'computerTest', 'submission_date',
                    'date_of_add', 'date_of_update', )
    list_display_links = ('student', 'id',)
    search_fields = ('student__first_name', 'student__last_name', 'id', 'competition__company__name', "description")
    readonly_fields = ('id', 'date_of_add', 'date_of_update', )
    ordering = ('-date_of_update',)
    filter_horizontal = ()
    autocomplete_fields = ['student', 'competition']
    list_filter = ('student', 'competition')
    fieldsets = ()


admin.site.register(Competitions, CompetitionsAdmin)
admin.site.register(ProgramGroup, ProgramGroupAdmin)
admin.site.register(EdProgram, EdProgramAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Contract, ContractAdmin)
admin.site.register(Applications, ApplicationsAdmin)

