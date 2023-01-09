from django.contrib import admin

# Register your models here.

from .models import Yoga

class YogaAdmin(admin.ModelAdmin):
    list_display = ('title','description','image')

admin.site.register(Yoga,YogaAdmin)
