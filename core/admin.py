from django.contrib import admin

from core import forms, models


class ConsultationAdmin(admin.ModelAdmin):
    form = forms.ConsultationForm


admin.site.register(models.Manager)
admin.site.register(models.Worker)
admin.site.register(models.Resident)
admin.site.register(models.District)
admin.site.register(models.Consultation, ConsultationAdmin)
admin.site.register(models.Action)
admin.site.register(models.Tool)
admin.site.register(models.Vehicle)
