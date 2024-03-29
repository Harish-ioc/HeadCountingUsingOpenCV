from django.contrib import admin
from . models import *

class MondayInline(admin.StackedInline):
    model=Monday
    extra=1

class TuesdayInline(admin.StackedInline):
    model=Tuesday
    extra=1

class WednesdayInline(admin.StackedInline):
    model=Wednesday
    extra=1

class ThursdayInline(admin.StackedInline):
    model=Thursday
    extra=1

class FridayInline(admin.StackedInline):
    model=Friday
    extra=1

class SaturdayInline(admin.StackedInline):
    model=Saturday
    extra=1


class TimeTableAdmin(admin.ModelAdmin):
    inlines=[MondayInline, TuesdayInline, WednesdayInline, ThursdayInline, FridayInline, SaturdayInline]
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'department':
            # setting the user from the request object
            kwargs['initial'] = request.user.id
            # making the field readonly
            kwargs['disabled'] = True
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # def save_model(self, request, obj, form, change):
    #     # Set the 'department' field to the current logged-in user's department when saving the model
    #     obj.department = request.user
    #     super().save_model(request, obj, form, change)
    

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Superusers can see all records

        # Filter records based on the logged-in user
        return qs.filter(department=request.user)

# Register your models here.
admin.site.register(TimeTable, TimeTableAdmin)
admin.site.register(Class)
admin.site.register(Branch)
admin.site.register(Teacher)
