from django.contrib import admin
from django.urls import path, include, re_path
from . import views
from django.views.generic import TemplateView
from rest_framework.authtoken.views import ObtainAuthToken

app_name = 'api_komax_app'

urlpatterns = [
    path('v1/auth/', ObtainAuthToken.as_view(), name='get_token'),
    path('v1/komaxes/', views.KomaxListView.as_view(), name='komax_list'),
    path('v1/komaxes/<str:number>/', views.KomaxDetailView.as_view(), name='komax_detail'),
    path('v1/kappas/', views.KappaListView.as_view(), name='kappa_list'),
    path('v1/kappas/<str:number>/', views.KappaDetailView.as_view(), name='kappa_detail'),
    path('v1/harnesses/', views.HarnessListView.as_view(), name='harness_list'),
    path('v1/harnesses/<str:harness_number>/', views.HarnessDetailView.as_view(), name='harness_detail'),
    path('v1/harness_chart/<str:harness_number>/', views.HarnessChartListView.as_view(), name='harness_chart_list'),
    path('komaxes_test/', views.index, name='index'),
]