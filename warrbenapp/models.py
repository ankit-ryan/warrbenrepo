from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.


class Project(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    ProjectName = models.CharField(max_length=120, null=True, blank=True)
    CompanyName = models.CharField(max_length=120, null=True, blank=True)
    ContactPerson = models.CharField(max_length=120, null=True, blank=True)
    ContactPersonDesignation = models.CharField(max_length=120, null=True, blank=True)
    Address = models.CharField(max_length=120, null=True, blank=True)
    PurposeValuation = models.CharField(max_length=120, null=True, blank=True)
    DateOfReport = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.ProjectName)

class EsopDetails(models.Model):
    YES_NO_choices = [('Yes', 'Yes'), ('No', 'No'), ('', '')]

    project = models.ForeignKey(Project, blank=True, null=True, on_delete=models.CASCADE)
    Grants = models.CharField(max_length=3, choices=YES_NO_choices, blank=True, null=True)
    GrantDate = models.DateField(null=True, blank=True)
    ESOPGranted = models.IntegerField(default=0)
    VestingOnMarket = models.CharField(max_length=3, choices=YES_NO_choices, blank=True, null=True)
    ValuationAvailable = models.CharField(max_length=3, choices=YES_NO_choices, blank=True, null=True)
    EquityValuePerShare  = models.FloatField(default=0)
    ExercisePrice = models.FloatField(default=0)
    CountryOfIncorporation = models.CharField(max_length=120, blank=True, null=True)
    DividendYield = models.FloatField(default=0)

    def __str__(self):
        return str(self.project)


class VestingXcel(models.Model):
    project = models.ForeignKey(Project, blank=True, null=True, on_delete=models.CASCADE)
    Vesting = models.CharField(max_length=50, null=True, blank=True, verbose_name='Vesting')
    VestingDate = models.DateField(null=True, blank=True, verbose_name='Vesting date')
    NumOfEsop = models.IntegerField(null=True, default=0, verbose_name='Number of ESOP vested')
    # PerEsop = models.FloatField(null= True, default=0, verbose_name='Percentage of ESOP vested')
    ExcerciseDate = models.DateField(null=True, blank=True, verbose_name='Exercise Date')


    def __str__(self):
        return str(self.project)

class VolatilityXcel(models.Model):
    project = models.ForeignKey(Project, blank=True, null=True, on_delete=models.CASCADE)
    ComparableCompany = models.CharField(max_length=50, null=True, blank=True)
    Ticker = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return str(self.project)



##########################################################################################################
class RiskExcel(models.Model):
    project = models.ForeignKey(Project, blank=True, null=True, on_delete=models.CASCADE)
    vesting = models.CharField(max_length=50, null=True, blank=True)
    period = models.FloatField(default=0.0)
    riskfree = models.FloatField(default=0.0)


    def __str__(self):
        return str(self.project)



class VolatilityAvgXcel(models.Model):
    project = models.ForeignKey(Project, blank=True, null=True, on_delete=models.CASCADE)
    comparablecompanies = models.CharField(max_length=50, null=True, blank=True)
    companyvolatilityAvg = models.FloatField(default=0.0)
    period = models.FloatField(default=0.0)
    TotalPeriodAvg = models.FloatField(default=0.0)


    def __str__(self):
        return str(self.project)
#########################################################################################################




class RiskFreeRate(models.Model):
    project = models.ForeignKey(Project, blank=True, null=True, on_delete=models.CASCADE)
    period = models.FloatField(default=0)
    riskfreerate = models.FloatField(default=0)
    VolatilityAverage = models.FloatField(default=0)

    def __str__(self):
        return str(self.project)


class FinalResult(models.Model):
    project = models.ForeignKey(Project, blank=True, null=True, on_delete=models.CASCADE)
    Type = models.CharField(max_length=50, null=True, blank=True)
    VestingDate = models.DateField(null=True, blank=True, verbose_name='Vesting date')
    NumOfEsop = models.IntegerField(default=0, verbose_name='Number of ESOP vested')
    PerEsop = models.FloatField(default=0, verbose_name='Percentage of ESOP vested')
    GrantDate = models.DateField(null=True, blank=True)
    VestingPeriod = models.FloatField(default=0.0)
    FairValueofShare = models.FloatField(default=0.0)
    ExcersisePrice = models.FloatField(default=0.0)
    RiskFRate = models.FloatField(default=0.0)
    Volatility = models.FloatField(default=0.0)
    DividendPayout = models.FloatField(default=0.0)
    FairValueofOption = models.FloatField(default=0.0)

    def __str__(self):
        return str(self.project)

