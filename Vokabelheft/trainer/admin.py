from django.contrib import admin
from .models import Dictionaries, Dictionary, Parts


@admin.register(Dictionaries)
class DictionariesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Parts)
class PartsAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Dictionary)
class DictionaryAdmin(admin.ModelAdmin):
    list_display = ('key', 'keyfonetic', 'word', 'form', 'plural', 'part', 'time_created', 'time_updated',
                    'language', 'moderate', 'user')
    list_filter = ('language', 'user')
    fieldsets = (
        (None, {
            'fields': ('key', 'keyfonetic', 'word')
        }),
        (None, {
            'fields': ('part', 'form', 'plural')
        })
    )


