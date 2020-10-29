from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import login
from . import views
from .views import ( RegisterView, DashboardView,
                    LoginView, PhoneVerificationView,
                    IndexView, log_out)
from django.contrib.auth import views as auth_views
from django.urls import path
from django.contrib.auth import views


urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index_page'),
    url(r'^register/$', RegisterView.as_view(), name="register_url"),
    url(r'^login/', LoginView.as_view(), name="login_url"),
    url(r'^verify/$', PhoneVerificationView, name="phone_verification_url"),
    url(r'^dashboard/$', DashboardView.as_view(), name="dashboard_url"),
    # url(r'^logout/$', logout.as_view(), {'next_page': '/'})
    url(r'^logout$', log_out, name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    # path('password_reset', views.PasswordResetView.as_view(), name='password_reset'),
    # url(r'^password_reset/$', views.PasswordResetView.as_view(), name='password_reset'),
    # url(r'^password_reset/done/$', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     views.PasswordResetConfirmView.as_view, name='password_reset_confirm'),
    # url(r'^reset/done/$', views.PasswordResetCompleteView.as_view, name='password_reset_complete'),


]