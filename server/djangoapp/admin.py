from django.contrib import admin
# from .models import related models
from .models import CarMake, CarModel

# Register your models here.

# CarModelInline class
# class CarModelInline(admin.StackedInline):
#     model = CarModel

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('modelname', 'type')
    list_filter = ['type']
    search_fields = ['modelname', 'type']

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    # inlines = [CarModelInline]
    list_display = ('name', 'description')
    list_filter = ['description']
    search_fields = ['name', 'description']

# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
