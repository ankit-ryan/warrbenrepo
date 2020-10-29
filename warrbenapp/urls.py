from . import views
from django.urls import path
from .views import (Pdf)

urlpatterns = [
    path('criotest', views.functest),
    path('EsopDetails/<str:Project_id>', views.Esopdetails, name='EsopDetails'),
    path('EsopDetails/Vestings/<str:Project_id>', views.Vestings, name='Vestings'),
    path('EsopDetails/Vestings/Vestings_excel/<str:Project_id>', views.Vestings_excel, name='Vestings_excel'),
    path('EsopDetails/Vestings/Volatility/<str:Project_id>', views.Volatility, name='Volatility'),
    path('EsopDetails/Vestings/Volatility/<str:Project_id>/Volatility_excel', views.Volatility_excel, name='Volatility_excel'),

    path('EsopDetails/Vestings/Volatility/Risk_free_Rate/VolatilityAnalysis/<str:Project_id>', views.Volatility_analysis, name='VolatilityAnalysis'),

    path('EsopDetails/Vestings/Volatility/Risk_free_Rate/VolatilityAnalysis/<str:Project_id>/Volatility_analysis_excel', views.Volatility_analysis_excel, name='Volatility_analysis_excel'),

    path('EsopDetails/Vestings/Volatility/Risk_free_Rate/VolatilityAnalysis/Analysis/<str:Project_id>', views.AnalysisResult, name='Analysis'),

    path('EsopDetails/Vestings/Volatility/Risk_free_Rate/<str:Project_id>', views.Risk_free_Rate, name='Risk_free_Rate'),

    path('EsopDetails/Vestings/Volatility/Risk_free_Rate/<str:Project_id>/Risk_free_Rate_excel', views.Risk_free_Rate_excel, name='Risk_free_Rate_excel'),
    # path('EsopDetails/Vestings/Volatility/Risk_free_Rate/VolatilityAnalysis/Analysis/<str:Project_id>/pdf', views.write_pdf_view)
    path('EsopDetails/Vestings/Volatility/Risk_free_Rate/VolatilityAnalysis/Analysis/<str:Project_id>/render/pdf/', Pdf.as_view()),
    path('projectview/', views.projectview, name = 'projectview'),
    path('themecheck', views.themecheck, name = 'themecheck'),
    # path('EsopDetails/Vestings/Volatility/VolatilityAnalysis/RiskRate/<str:Project_id>', views.RiskRate, name='RiskRate'),
    # path('EsopDetails/Vestings/Volatility/RiskRate/Analysis/<str:Project_id>', views.AnalysisResult, name='Analysis'),
]