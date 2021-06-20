from django.contrib import admin
from .models import Snippet


# Register your models here.

@admin.register(Snippet)
class SnippetModel(admin.ModelAdmin):
    list_display = ['code']
