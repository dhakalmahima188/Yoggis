from django.contrib import admin


from .models import Yoga, YogaScore, UserDisorder, YogaCategory, CorrectVectorLocations,SUserDisorder


class YogaAdmin(admin.ModelAdmin):  #inherited from ModelAdmin
    list_display = ('title', 'difficulty',)


class YogaScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'yoga', 'score',)


class CorrectVectorLocationsAdmin(admin.ModelAdmin):
    list_display = ('angle_of',)
    
# class SuserDisorderAdmin(admin.ModelAdmin):
#     list_display=('user','disorder')


admin.site.register(Yoga, YogaAdmin)
admin.site.register(YogaScore, YogaScoreAdmin)
admin.site.register(UserDisorder)
# admin.site.register(SUserDisorder,SuserDisorderAdmin)
admin.site.register(SUserDisorder)
admin.site.register(YogaCategory)
admin.site.register(CorrectVectorLocations, CorrectVectorLocationsAdmin)
