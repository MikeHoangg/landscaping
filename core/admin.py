from django.contrib import admin
from django.contrib.auth.models import User, Group

from core import forms, models


class ActionInline(admin.StackedInline):
    model = models.Action
    extra = 1
    filter_horizontal = ('workers',)


class ConsultationAdmin(admin.ModelAdmin):
    search_fields = (
        'date',
        'district__district_type',
        'district__name',
    )
    list_display = (
        'date',
        'district',
    )
    form = forms.ConsultationForm
    filter_horizontal = ('residents',)

    inlines = (ActionInline,)


class ActionAdmin(admin.ModelAdmin):
    search_fields = (
        'date',
        'consultation__district__district_type',
        'consultation__district__name',
    )
    list_display = (
        'date',
        'consultation',
        'description'
    )
    filter_horizontal = ('workers',)


class VehicleAdmin(admin.ModelAdmin):
    filter_horizontal = ('workers',)


admin.site.unregister(User)
admin.site.unregister(Group)

admin.site.register(models.Manager)
admin.site.register(models.Worker)
admin.site.register(models.Resident)
admin.site.register(models.District)
admin.site.register(models.Consultation, ConsultationAdmin)
admin.site.register(models.Action, ActionAdmin)
admin.site.register(models.Tool)
admin.site.register(models.Vehicle, VehicleAdmin)
