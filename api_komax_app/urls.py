from django.contrib import admin
from django.urls import path, include, re_path
from . import views
from django.views.generic import TemplateView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.routers import DefaultRouter
from .viewsets import KomaxViewSet, KappaViewSet, HarnessViewSet, LabourisnessViewSet, KomaxTerminalsViewSet, \
    KomaxStatusViewSet, HarnessChartViewSet, KomaxSealViewSet, WorkerViewSet

app_name = 'api_komax_app'

router = DefaultRouter()
router.register('komaxes', KomaxViewSet)
router.register('kappas', KappaViewSet)
router.register('harnesses', HarnessViewSet)
router.register('laboriousness', LabourisnessViewSet)
router.register('komax_terminals', KomaxTerminalsViewSet)
router.register('komax_status', KomaxStatusViewSet)
router.register('harness_chart', HarnessChartViewSet)
router.register('komax_seals', KomaxSealViewSet)
router.register('workers', WorkerViewSet)


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
    path('v2/komax_tasks/', views.KomaxTaskListView.as_view(), name='komax_tasks_list'),
    path('v2/', include(router.urls)),
]