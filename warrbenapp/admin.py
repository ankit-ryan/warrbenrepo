from django.contrib import admin
from .models import Project, EsopDetails, VestingXcel, VolatilityXcel, RiskFreeRate, VolatilityAvgXcel, RiskExcel, FinalResult
from import_export.admin import ImportExportModelAdmin
# Register your models here.


admin.site.register(Project)
admin.site.register(EsopDetails)
admin.site.register(VolatilityXcel)
admin.site.register(RiskFreeRate)
admin.site.register(VolatilityAvgXcel)
admin.site.register(RiskExcel)
admin.site.register(FinalResult)



@admin.register(VestingXcel)
class VestingXcelAdmin(ImportExportModelAdmin):
    list_display = ('project', 'Vesting', 'VestingDate', 'NumOfEsop', 'ExcerciseDate')