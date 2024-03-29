from django.contrib import admin
from django.db.models import Q
from django.utils import timezone
from . models import *
from django import forms


class DataInline(admin.StackedInline):
    model = Data
    extra=1

class DataAdmin(admin.ModelAdmin):
    list_display = ('date', 'period', 'cam', 'count')


class CameraAdminForm(forms.ModelForm):
    start_date = forms.DateField(required=False, label='Start Date')
    end_date = forms.DateField(required=False, label='End Date')
    period = forms.ChoiceField(choices=[('p1', 'p1'), ('p2', 'p2'), ('p3', 'p3'), ('p4', 'p4'), ('p5', 'p5'),
                                        ('p6', 'p6'), ('p7', 'p7'), ('p8', 'p8'), ('p9', 'p9'), ('p10', 'p10')],
                               required=False, label='Period')

    class Meta:
        model = Camera
        fields = '__all__'

class CameraAdmin(admin.ModelAdmin):
    inlines = [DataInline]
    list_display = ('name', 'block', 'ip', 'usr', 'pwd')
    list_filter = ('block', 'name', 'ip')  # Add any other fields you want to filter on
    form = CameraAdminForm

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        period = request.GET.get('period')

        if start_date and end_date and period:
            queryset |= self.model.objects.filter(
                data__date__date__range=[start_date, end_date],
                data__period=period
            )

        return queryset, use_distinct


class MinutesInline(admin.StackedInline):
    model = Minutes
    extra = 1

class SecondsInline(admin.StackedInline):
    model = Seconds
    extra = 1

class TimePeriodInline(admin.StackedInline):
    model = TimePeriod
    extra = 1

class SnapsAdmin(admin.ModelAdmin):
    inlines=[MinutesInline, SecondsInline, TimePeriodInline]

# Register your models here.
admin.site.register(Block)
admin.site.register(Camera, CameraAdmin)
admin.site.register(Data, DataAdmin)
admin.site.register(Snaps, SnapsAdmin)