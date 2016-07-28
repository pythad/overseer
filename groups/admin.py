from django.contrib import admin
from .models import DistributorGroup


@admin.register(DistributorGroup)
class DistributorGroupAdmin(admin.ModelAdmin):
	pass
