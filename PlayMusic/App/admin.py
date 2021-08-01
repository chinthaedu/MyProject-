from django.contrib import admin
from .models import Movie
from import_export.admin import ImportExportModelAdmin

@admin.register(Movie)
class ViewAdmin(ImportExportModelAdmin):
	pass