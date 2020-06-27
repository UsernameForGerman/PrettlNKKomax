from django.contrib import admin
from django.urls import path, include, re_path
from . import views
from django.views.generic import TemplateView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.routers import DefaultRouter
from .viewsets import KomaxViewSet, KappaViewSet, HarnessViewSet, LabourisnessViewSet, KomaxTerminalsViewSet, \
    KomaxStatusViewSet, HarnessChartViewSet, KomaxSealViewSet, WorkerViewSet

app_name = 'api'

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
    path('index/', views.index, name='index'),
    path('v2/login/', ObtainAuthToken.as_view(), name='get_token'),
    path('v2/logout/', views.Logout.as_view(), name='logout'),
    path('v2/komax_tasks/', views.KomaxTaskListView.as_view(), name='komax_tasks_list'),
    path('v2/load_komax_task/', views.LoadTaskView.as_view(), name='load-komax-task'),
    path('v2/send_komax_task/', views.SendTaskView.as_view(), name='send-komax-task'),
    path('v2/worker_account/', views.WorkerAccountView.as_view(), name='worker-account'),
    path('v2/komax_task_status/', views.TaskStatusView.as_view(), name='komax-task-status'),
    # path('v2/xlsx_task/', views.XlsxTaskView.as_view(), name='xlsx-task'),
    path('v2/', include(router.urls)),
]