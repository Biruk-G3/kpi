from django.contrib import admin

from .models import KpiDetails, Kpi

# Register your models here.
admin.site.register(Kpi)
admin.site.register(KpiDetails)