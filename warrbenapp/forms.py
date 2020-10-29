from django import forms


class Projectform(forms.Form):

    Project_Name = forms.CharField(max_length=120, label='')
    Name_of_Company_Issuing_ESOPs = forms.CharField(max_length=120, label='')
    Contact_Person = forms.CharField(max_length=120, label='')
    Contact_Person_Designation = forms.CharField(max_length=120, label='')
    Address = forms.CharField(max_length=120, label='')
    Purpose_of_Valuation = forms.CharField(max_length=120, label='')
    Date_of_Report = forms.DateField(label='', widget=forms.TextInput(attrs=
                                {
                                    'class':'datepicker'
                                }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Project_Name'].widget.attrs.update({'class': 'feedback-input', 'placeholder': 'Project Name'})
        self.fields['Name_of_Company_Issuing_ESOPs'].widget.attrs.update({'class': 'feedback-input', 'placeholder': 'Name of Company Issuing ESOPs'})
        self.fields['Contact_Person'].widget.attrs.update({'class': 'feedback-input', 'placeholder': 'Contact Person'})
        self.fields['Contact_Person_Designation'].widget.attrs.update({'class': 'feedback-input', 'placeholder': 'Contact Person designation'})
        self.fields['Address'].widget.attrs.update({'class': 'feedback-input', 'placeholder': 'Address'})
        self.fields['Purpose_of_Valuation'].widget.attrs.update({'class': 'feedback-input', 'placeholder': 'Purpose of Valuation'})
        self.fields['Date_of_Report'].widget.attrs.update({'class': 'datepicker', 'placeholder': 'Date Of Report'})


class Esopform(forms.Form):
    TRUE_FALSE_CHOICES = (
        (True, 'Yes'),
        (False, 'No')
    )

    Are_there_multiple_grants = forms.ChoiceField(choices = TRUE_FALSE_CHOICES, widget=forms.Select(), label='Are there multiple grants?')
    Grant_Date = forms.DateField(label='', widget=forms.TextInput(attrs=
                                {
                                    'class':'datepicker'
                                }))

    Number_Of_ESOPs_granted = forms.IntegerField(label='')
    Is_Vesting_Based_On_Market_Condition = forms.ChoiceField(choices = TRUE_FALSE_CHOICES, widget=forms.Select(), label='Is Vesting Based On Market Condition?')
    Is_Company_Equity_Valuation_Available = forms.ChoiceField(choices = TRUE_FALSE_CHOICES, widget=forms.Select(), label='Is Company Equity Valuation Available?')
    Company_Common_Equity_Value_Per_Share = forms.FloatField(label='')
    Exercise_Price = forms.FloatField(label='')
    Country_Of_Incorporation = forms.CharField(max_length=120, label='')
    Dividend_Yield = forms.FloatField(label='')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Are_there_multiple_grants'].widget.attrs.update({'class': 'feedback-input'})
        self.fields['Grant_Date'].widget.attrs.update({'class': 'datepicker', 'placeholder': 'Grant Date?'})
        self.fields['Number_Of_ESOPs_granted'].widget.attrs.update({'class': 'feedback-input', 'placeholder': 'Number Of Esops Granted'})
        self.fields['Is_Vesting_Based_On_Market_Condition'].widget.attrs.update({'class': 'feedback-input'})
        self.fields['Is_Company_Equity_Valuation_Available'].widget.attrs.update({'class': 'feedback-input'})
        self.fields['Company_Common_Equity_Value_Per_Share'].widget.attrs.update({'class': 'feedback-input', 'placeholder': 'Company Common Equity Value Per Share'})
        self.fields['Exercise_Price'].widget.attrs.update({'class': 'feedback-input', 'placeholder': 'Exercise Price'})
        self.fields['Country_Of_Incorporation'].widget.attrs.update({'class': 'feedback-input', 'placeholder': 'Country Of Incorporation'})
        self.fields['Dividend_Yield'].widget.attrs.update({'class': 'feedback-input', 'placeholder': 'Dividend Yield'})

class Volatilityform(forms.Form):
    Comparable_Company = forms.CharField(max_length=120, label='')
    Ticker = forms.CharField(max_length=120, label='')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Comparable_Company'].widget.attrs.update({'class': 'feedback-input', 'placeholder': 'Comparable Company'})
        self.fields['Ticker'].widget.attrs.update({'class': 'feedback-input', 'placeholder': 'Ticker'})



class RiskFreeRateform(forms.Form):
    Risk_Free_Rate = forms.FloatField(label='Risk Free Rate')
    Volatility_Average = forms.FloatField(label='Volatility Average')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Risk_Free_Rate'].widget.attrs.update({'class': 'feedback-input', 'placeholder': 'Risk Free Rate'})
        self.fields['Volatility_Average'].widget.attrs.update({'class': 'feedback-input', 'placeholder': 'Volatility Average'})