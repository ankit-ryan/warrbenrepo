from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .forms import Projectform, Esopform, Volatilityform, RiskFreeRateform
from .models import Project, EsopDetails, VolatilityXcel, VestingXcel, RiskFreeRate, VolatilityAvgXcel, RiskExcel, FinalResult
from django.shortcuts import redirect
import xlwt
from tablib import Dataset
from .resources import VestingXcelResource, VolatilityXcelResource, VolatilityAvgXcelResource, RiskExcelResource
import datetime
from scipy import log, exp, sqrt, stats
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table
from reportlab.platypus import TableStyle
from reportlab.lib import colors
from .render import Render
from django.views.generic import View
from .render import Render
import xlsxwriter
import io
from django.contrib import messages
# Create your views here.

@login_required(login_url="/login/")
def functest(request):
    msg = ''
    form = Projectform(request.POST or None)
    if form.is_valid():
        msg= "Form submitted"
        obj1 = Project()
        obj1.user = request.user
        obj1.ProjectName = form.cleaned_data['Project_Name']
        obj1.CompanyName = form.cleaned_data['Name_of_Company_Issuing_ESOPs']
        obj1.ContactPerson = form.cleaned_data['Contact_Person']
        obj1.ContactPersonDesignation = form.cleaned_data['Contact_Person_Designation']
        obj1.Address = form.cleaned_data['Address']
        obj1.PurposeValuation = form.cleaned_data['Purpose_of_Valuation']
        obj1.DateOfReport = form.cleaned_data['Date_of_Report']
        obj1.save()
        ob = obj1.id
        print("ob", ob)
        url2 = "EsopDetails/" + str(ob)
        return redirect(url2)
    return render(request, 'Create_Project.html', {'form':form, 'msg':msg})

@login_required(login_url="/login/")
def Esopdetails(request, Project_id):
    Project_id = int(Project_id)
    var = Project.objects.get(id = Project_id)
    msg = ''
    form = Esopform(request.POST or None)
    if form.is_valid():
        msg = "Form submitted"
        # obj = EsopDetails.objects.all()
        # for i in obj:
        #     ob = i.Project_id

        obj1 = EsopDetails()
        obj1.project = var
        obj1.Grants = form.cleaned_data['Are_there_multiple_grants']
        obj1.GrantDate = form.cleaned_data['Grant_Date']
        obj1.ESOPGranted = form.cleaned_data['Number_Of_ESOPs_granted']
        obj1.VestingOnMarket = form.cleaned_data['Is_Vesting_Based_On_Market_Condition']
        obj1.ValuationAvailable = form.cleaned_data['Is_Company_Equity_Valuation_Available']
        obj1.EquityValuePerShare = form.cleaned_data['Company_Common_Equity_Value_Per_Share']
        obj1.ExercisePrice = form.cleaned_data['Exercise_Price']
        obj1.CountryOfIncorporation = form.cleaned_data['Country_Of_Incorporation']
        obj1.DividendYield = form.cleaned_data['Dividend_Yield']
        obj1.save()
        url2 = "Vestings/" + str(Project_id)
        return redirect(url2)
    projectlist = EsopDetails.objects.filter(project = Project_id)
    return render(request, 'Esop_Details.html', {'form': form, 'msg': msg, 'Project_id':Project_id, 'projectlist':projectlist})


@login_required(login_url="/login/")
def Vestings(request, Project_id):
    Project_id = int(Project_id)
    error = ""
    if request.method == 'POST':
        input_resource = VestingXcelResource()
        dataset = Dataset()
        new_input = request.FILES['myFile']if 'myFile' in request.FILES else None
        if new_input is None:
            error = 'Please choose file!'
        else:
            error_first2 = False
            error_rest = False
            imported_data = dataset.load(new_input.read(), format='xlsx')
            print('imported_data', imported_data)
            for data in imported_data:
                data = list(data)
                print('data', data)
                for column in [2,3,4,5]:
                    if data[column] is None:
                        error_rest = True
                if data[0] is not None or data[1] is not None:
                    error_first2 = True
            if error_rest:
                messages.error(request, 'Please upload the data in proper format')
            if error_first2:
                messages.error(request, 'Please leave the id and project column blank')

            print('first',error_first2,'rest',error_rest)
            if (error_first2 == False) & (error_rest == False):
                print("enter")
                for data in imported_data:
                    data = list(data)

                    data[1] = Project_id
                    value = VestingXcel(
                        data[0],
                        data[1],
                        data[2],
                        data[3],
                        data[4],
                        data[5],
                    )
                    value.save()
                url2 = "Volatility/" + str(Project_id)
                return redirect(url2)
    projectlist = VestingXcel.objects.filter(project=Project_id)
    print(error)
    return render(request, 'Vesting.html', {'error': error, 'Project_id':Project_id, 'projectlist': projectlist})

@login_required(login_url="/login/")
def Vestings_excel(request, Project_id):
    # Create a workbook and add a worksheet.
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()

    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': 1})
    white = workbook.add_format({'bold': True, 'font_color': 'white'})
    # Add a number format for cells with money.
    money_format = workbook.add_format({'num_format': '$#,##0'})

    # Add an Excel date format.
    date_format = workbook.add_format({'num_format': 'mmmm d yyyy'})

    # Adjust the column width.
    worksheet.set_column(1, 1, 15)

    # Write some data headers.
    worksheet.write('A1', 'id', bold)
    worksheet.write('B1', 'project', bold)
    worksheet.write('C1', 'Vesting', bold)
    worksheet.write('D1', 'Vesting date', bold)
    worksheet.write('E1', 'Number of ESOP vested', bold)
    worksheet.write('F1', 'Exercise Date', bold)

    workbook.close()
    output.seek(0)

    filename = 'Vesting.xlsx'
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response


@login_required(login_url="/login/")
def Volatility(request, Project_id):
    Project_id = int(Project_id)
    error = ""
    if request.method == 'POST':
        input_resource = VolatilityXcelResource()
        dataset = Dataset()
        new_input = request.FILES['myFile'] if 'myFile' in request.FILES else None
        if new_input is None:
            error = 'Please choose file!'
        else:
            error_first2 = False
            error_rest = False
            imported_data = dataset.load(new_input.read(), format='xlsx')
            print('imported_data', imported_data)
            for data in imported_data:
                data = list(data)
                print('data', data)
                for column in [2, 3]:
                    print(data[column])
                    if data[column] is None:
                        error_rest = True
                if data[0] is not None or data[1] is not None:
                    error_first2 = True
            if error_rest:
                messages.error(request, 'Please upload the data in proper format')
            if error_first2:
                messages.error(request, 'Please leave the id and project column blank')

            print('first', error_first2, 'rest', error_rest)
            if (error_first2 == False) & (error_rest == False):
                for data in imported_data:
                    data = list(data)
                    data[1] = Project_id
                    value = VolatilityXcel(
                        data[0],
                        data[1],
                        data[2],
                        data[3]
                    )
                    value.save()
                url2 = "Risk_free_Rate/" + str(Project_id)
                return redirect(url2)
    projectlist = VolatilityXcel.objects.filter(project=Project_id)
    return render(request, 'Volatility.html', {'error': error, 'Project_id':Project_id, 'projectlist': projectlist})

@login_required(login_url="/login/")
def Volatility_excel(request, Project_id):
    # Create a workbook and add a worksheet.
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()

    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': 1})
    white = workbook.add_format({'bold': True, 'font_color': 'white'})
    # Add a number format for cells with money.
    money_format = workbook.add_format({'num_format': '$#,##0'})

    # Add an Excel date format.
    date_format = workbook.add_format({'num_format': 'mmmm d yyyy'})

    # Adjust the column width.
    worksheet.set_column(1, 1, 15)

    # Write some data headers.
    worksheet.write('A1', 'id', bold)
    worksheet.write('B1', 'project', bold)
    worksheet.write('C1', 'Comparable Company', bold)
    worksheet.write('D1', 'Ticker', bold)

    workbook.close()
    output.seek(0)

    filename = 'Volatility.xlsx'
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response

#####################################################################################################
@login_required(login_url="/login/")
def Volatility_analysis(request, Project_id):
    Project_id = int(Project_id)
    # var_2 = RiskExcel.objects.filter(project = Project_id)
    var_2 = RiskExcel.objects.filter(project = Project_id).values_list('period', flat=True).distinct()
    for i in var_2:
        print('period',i)

    error = ""
    if request.method == 'POST':
        input_resource = VolatilityAvgXcelResource()
        dataset = Dataset()
        new_input = request.FILES['myFile'] if 'myFile' in request.FILES else None
        if new_input is None:
            error = 'Please choose file!'
        else:
            error_first2 = False
            error_rest = False
            imported_data = dataset.load(new_input.read(), format='xlsx')
            print('imported_data', imported_data)
            for data in imported_data:
                data = list(data)
                print('data', data)
                for column in [2, 3, 4]:
                    print(data[column])
                    if data[column] is None:
                        error_rest = True
                if data[0] is not None or data[1] is not None:
                    error_first2 = True
            if error_rest:
                messages.error(request, 'Please upload the data in proper format')
            if error_first2:
                messages.error(request, 'Please leave the id and project column blank')

            print('first', error_first2, 'rest', error_rest)
            if (error_first2 == False) & (error_rest == False):
                avg = []
                for idx,i in enumerate(var_2):
                    sum = 0
                    number = 0
                    for data in imported_data:
                        sum += data[3+idx]
                        number += 1
                    avg.append(sum/number)

                print(avg)
                for data in imported_data:
                    data = list(data)
                    print('data', data)
                    data[1] = Project_id
                    for idx,i in enumerate(var_2):

                        value = VolatilityAvgXcel(
                        data[0],
                        data[1],
                        data[2],
                        data[3+idx],
                        i,
                        avg[idx]
                        )
                        value.save()
                    print('save')
                url2 = "Analysis/" + str(Project_id)
                return redirect(url2)
    projectlist = VolatilityAvgXcel.objects.filter(project=Project_id)
    return render(request, 'VolatilityAnalysis.html', {'error': error, 'Project_id':Project_id, 'projectlist': projectlist})

@login_required(login_url="/login/")
def Volatility_analysis_excel(request, Project_id):
    Project_id = int(Project_id)
    var = VestingXcel.objects.filter(project=Project_id)
    grant = EsopDetails.objects.filter(project=Project_id)
    grant_date = grant[0].GrantDate
    var_2 = VolatilityXcel.objects.filter(project=Project_id)
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()

    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': 1})

    # Add a number format for cells with money.
    money_format = workbook.add_format({'num_format': '$#,##0'})

    # Add an Excel date format.
    date_format = workbook.add_format({'num_format': 'mmmm d yyyy'})

    # Adjust the column width.
    worksheet.set_column(1, 1, 15)

    row_num = 0
    columns = ['id', 'project', 'comparable companies']
    for i in var:
        a = (((i.ExcerciseDate - i.VestingDate) / 365) / 2) + ((i.VestingDate - grant_date) / 365)
        hours = a.days + a.seconds / 60 / 60 / 24
        columns.append(hours)

    for col_num in range(len(columns)):
        worksheet.write(row_num, col_num, columns[col_num], bold)

    col_num = 2
    for row_num in range(len(var_2)):
        worksheet.write(row_num + 1, col_num, var_2[row_num].ComparableCompany)

    workbook.close()
    output.seek(0)

    filename = 'VolatilityAnalysis.xlsx'
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response
#########################################################################################################################


@login_required(login_url="/login/")
def Risk_free_Rate(request, Project_id):
    print('pro1', Project_id)
    Project_id = int(Project_id)
    var = VestingXcel.objects.filter(project=Project_id)
    grant = EsopDetails.objects.filter(project=Project_id)

    if len(grant) == 0:
        messages.error(request, "Please enter the form in proper sequence")
    else:
        grant_date = grant[0].GrantDate
        error = ""
        if request.method == 'POST':
            input_resource = RiskExcelResource()
            dataset = Dataset()
            new_input = request.FILES['myFile'] if 'myFile' in request.FILES else None
            if new_input is None:
                error = 'Please choose file!'
            else:
                error_first2 = False
                error_rest = False
                imported_data = dataset.load(new_input.read(), format='xlsx')
                print('imported_data', imported_data)
                for data in imported_data:
                    data = list(data)
                    print('data', data)
                    for column in [2, 3, 4]:
                        print(data[column])
                        if data[column] is None:
                            error_rest = True
                    if data[0] is not None or data[1] is not None:
                        error_first2 = True
                if error_rest:
                    messages.error(request, 'Please upload the data in proper format')
                if error_first2:
                    messages.error(request, 'Please leave the id and project column blank')

                print('first', error_first2, 'rest', error_rest)
                if (error_first2 == False) & (error_rest == False):
                    for idx,data in enumerate(imported_data):
                        data = list(data)
                        print('data', data)
                        data[1] = Project_id
                        data[2] = var[idx].Vesting
                        a = (((var[idx].ExcerciseDate - var[idx].VestingDate) / 365) / 2) + ((var[idx].VestingDate - grant_date) / 365)
                        hours = a.days + a.seconds / 60 / 60 / 24
                        data[3] = hours
                        value = RiskExcel(
                        data[0],
                        data[1],
                        data[2],
                        data[3],
                        data[4]
                        )
                        print("inside for",data)
                        value.save()
                    url2 = "VolatilityAnalysis/" + str(Project_id)
                    return redirect(url2)
    projectlist = RiskExcel.objects.filter(project=Project_id)
    return render(request, 'RiskFreeRateExcel.html', {'Project_id': Project_id, 'projectlist': projectlist})





@login_required(login_url="/login/")
def Risk_free_Rate_excel(request, Project_id):
    # Create a workbook and add a worksheet.
    var = VestingXcel.objects.filter(project=Project_id)
    grant = EsopDetails.objects.filter(project=Project_id)
    grant_date = grant[0].GrantDate
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()

    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': 1})
    white = workbook.add_format({'bold': True, 'font_color': 'white'})
    # Add a number format for cells with money.
    money_format = workbook.add_format({'num_format': '$#,##0'})

    # Add an Excel date format.
    date_format = workbook.add_format({'num_format': 'mmmm d yyyy'})

    # Adjust the column width.
    worksheet.set_column(1, 1, 15)

    row_num = 0
    columns = ['id', 'project', 'Vesting', 'Period', 'Risk free Rate']

    for i in var:
        a = (((i.ExcerciseDate - i.VestingDate) / 365) / 2) + ((i.VestingDate - grant_date) / 365)
        hours = a.days + a.seconds / 60 / 60 / 24

    for col_num in range(len(columns)):
        worksheet.write(row_num, col_num, columns[col_num], bold)

    col_num = 2
    for row_num in range(len(var)):
        worksheet.write(row_num + 1, 2, var[row_num].Vesting)
        worksheet.write(row_num + 1, 3, hours)

    # Write some data headers.
    # worksheet.write('A1', 'id', bold)
    # worksheet.write('B1', 'project', bold)
    # worksheet.write('C1', 'Vesting', bold)
    # worksheet.write('D1', 'Period', bold)
    # worksheet.write('E1', 'Risk free Rate', bold)

    workbook.close()
    output.seek(0)

    filename = 'RiskFreeRate.xlsx'
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response



def defbs_call(S,div, X, T, r, sigma):
         r = r/100
         sigma = sigma/100
         d1 = (log(S / X) + (r - div + sigma * sigma / 2.) * T) / (sigma * sqrt(T))
         d2 = d1 - sigma * sqrt(T)
         return ((S * stats.norm.cdf(d1)*exp(-div*T)) - (X * exp(-r * T) * stats.norm.cdf(d2)))

def comp_is_in(comp,comp_volatility):
    found = -1
    for idx,i in enumerate(comp_volatility):
        if i[0] == comp:
            found = idx
    return found

@login_required(login_url="/login/")
def AnalysisResult(request, Project_id):

    Project_id = int(Project_id)
    pid = Project.objects.get(id=Project_id)
    var = VolatilityXcel.objects.filter(project = pid)
    var2 = VolatilityAvgXcel.objects.filter(project = pid)
    num = VolatilityAvgXcel.objects.filter(project = pid).values_list('period', flat=True).distinct()
    num2 = VolatilityAvgXcel.objects.filter(project = pid).values_list('comparablecompanies', flat=True).distinct()
    var3 = VestingXcel.objects.filter(project = pid)
    var4 = EsopDetails.objects.filter(project = pid)
    var6 = RiskExcel.objects.filter(project = pid)
    var5 = []
    period_to_vol_avg = {}
    comp_volatility = []
    for i in var2:
        idx = comp_is_in(i.comparablecompanies,comp_volatility)
        if idx == -1:
            next_entry = [i.comparablecompanies,i.companyvolatilityAvg]
            comp_volatility.append(next_entry)
        else:
            comp_volatility[idx].append(i.companyvolatilityAvg)
    for i in var2:
        period_to_vol_avg[i.period] = i.TotalPeriodAvg
    print(period_to_vol_avg)


    final = FinalResult.objects.filter(project = pid)
    # no_of_vesting = 0
    # for i in final:
    #     no_of_vesting += 1
    # if no_of_vesting > 0:
    #     condition = 0
    for i in final:
        i.delete()

    for index,i in enumerate(var6):
        dividend = var4[0].DividendYield
        exercise = var4[0].ExercisePrice
        fair_value = var4[0].EquityValuePerShare
        term = i.period
        volatility = period_to_vol_avg[term]
        risk_free = i.riskfree
        fair_option = defbs_call(fair_value,dividend,exercise,term,risk_free,volatility)
        var5.append(fair_option)

        vesting = var3[index].Vesting
        vestingdate = var3[index].VestingDate
        numbofesop = var3[index].NumOfEsop
        peresop = (numbofesop/var4[0].ESOPGranted)*100

        grantdate = var4[0].GrantDate

        obj1 = FinalResult()

        obj1.project = pid
        obj1.Type = vesting
        obj1.VestingDate = vestingdate
        obj1.NumOfEsop = numbofesop
        obj1.PerEsop = peresop
        obj1.GrantDate = grantdate
        obj1.VestingPeriod = term
        obj1.FairValueofShare = fair_value
        obj1.ExcersisePrice = exercise
        obj1.RiskFRate = risk_free
        obj1.Volatility = volatility
        obj1.DividendPayout = dividend
        obj1.FairValueofOption = fair_option
        obj1.save()


    var7 = FinalResult.objects.filter(project = pid)
    projectlist = FinalResult.objects.filter(project=Project_id)
    return render(request, 'Result.html', {'var':var, 'var2':var2, 'var3':var3, 'var4':var4, 'var5':var5, 'var7':var7, 'Project_id': Project_id, 'num': num, 'num2': num2, 'comp_volatility': comp_volatility, 'projectlist': projectlist })

class Pdf(View):

    def get(self, request, Project_id):
        Project_id = int(Project_id)
        print('pro', Project_id)
        pid = Project.objects.get(id=Project_id)
        print('id', pid)
        data = FinalResult.objects.filter(project = pid)
        pid2 = Project.objects.filter(id = Project_id)
        for i in pid2:
            print('company', i.CompanyName)
        pid3 = EsopDetails.objects.filter(project = pid)

        params = {
            'pid3': pid3,
            'pid':pid2,
            'sales': data,
            'request': request
        }
        return Render.render('pdf_template.html', params)

@login_required(login_url="/login/")
def projectview(request):
    projectlist = Project.objects.filter(user = request.user)
    return render(request, 'ProjectList.html', {'projectlist': projectlist} )

def themecheck(request):
    return render(request, 'base.html')