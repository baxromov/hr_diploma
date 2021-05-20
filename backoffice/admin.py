from django.contrib import admin
from app import models


@admin.register(models.WorlPlan)
class WorkPlanAdmin(admin.ModelAdmin):
    pass