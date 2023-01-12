from django.contrib import admin

# Register your models here.

from .models import Yoga, YogaScore, UserDisorder, YogaCategory, CorrectVectorLocations

admin.site.register(Yoga)
admin.site.register(YogaScore)
admin.site.register(UserDisorder)
admin.site.register(YogaCategory)
admin.site.register(CorrectVectorLocations)