from django.contrib import admin
from .models import DistributorPerson


@admin.register(DistributorPerson)
class DistributorPersonAdmin(admin.ModelAdmin):
	pass
