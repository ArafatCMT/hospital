from django.contrib import admin
from . import models

# Register your models here.

class DesignationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'slug']

class SpecializationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'slug']

admin.site.register(models.Designation, DesignationAdmin)
admin.site.register(models.Specialization, SpecializationAdmin)
admin.site.register(models.AvailableTime)
admin.site.register(models.Doctor)
admin.site.register(models.Review)
