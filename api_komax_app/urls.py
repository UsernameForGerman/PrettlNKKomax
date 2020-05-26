from django.contrib import admin
from django.urls import path, include, re_path
from . import views
from django.views.generic import TemplateView

app_name = 'api_komax_app'

urlpatterns = [
    path('v1/komaxes/', views.EquipmentListView.as_view(), name='equipment_list'),
    path('komaxes_test/', views.index, name='index'),
]