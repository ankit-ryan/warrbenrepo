from import_export import resources, widgets
from import_export.fields import Field
from .models import VestingXcel, Project, VolatilityXcel, VolatilityAvgXcel, RiskExcel
from django.forms import ValidationError



class VestingXcelResource(resources.ModelResource):
    # project_id = Field(column_name='project', attribute='project', widget=widgets.ForeignKeyWidget(Project))
    # Vesting = Field(column_name='Vesting', attribute='Vesting')
    # VestingDate = Field(column_name='Vesting Date', attribute='Vesting Date')
    # NumOfEsop = Field(column_name='Number of ESOP vested', attribute='Number of ESOP vested')
    # PerEsop = Field(column_name='Persentage of ESOP vested', attribute='Persentage of ESOP vested')
    # ExcerciseDate = Field(column_name='Exercise Date', attribute='Exercise Date')
    #

    class Meta:
        model = VestingXcel
    #     fields = ('id', 'project_id', 'Vesting', 'VestingDate', 'NumOfEsop', 'PerEsop', 'ExcerciseDate')
    #
    # def before_import_row(self, row, **kwargs):
    #     value = row['project']
    #     obj = Project.objects.filter(project=value)
    #     for i in obj:
    #         row['project'] = i.id


class VolatilityXcelResource(resources.ModelResource):

    class Meta:
        model = VolatilityXcel



class VolatilityAvgXcelResource(resources.ModelResource):

    class Meta:
        model = VolatilityAvgXcel


class RiskExcelResource(resources.ModelResource):

    class Meta:
        model = RiskExcel
