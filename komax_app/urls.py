from django.contrib import admin
from django.urls import path, include, re_path
from . import views
from django.views.generic import TemplateView

app_name = 'komax_app'

urlpatterns = [
    re_path(r'^$', views.komax_app_view, name='komax_app_view'),
    re_path(r'^komax_tasks/(?P<task_name>[a-zA-Z0-9_.-]*)/$', views.KomaxTaskView.as_view(), name='task_view'),
    re_path(r'^setup/$', views.KomaxAppSetupView.as_view(), name='task_setup'),
    re_path(r'^komax_tasks/(?P<pk>\d+[\w-]+)/amount/$', views.set_amount_task_view, name='task_amount'),
    re_path(r'^komax_tasks/(?P<task_name>[a-zA-Z0-9_.-]*)/get_task/$', views.get_general_task_view, name='get_task'),
    re_path(r'^komax_tasks/(?P<task_name>[a-zA-Z0-9_.-]*)/get_tech_task$', views.get_general_tech_task_view, name='get_tech_task'),
    re_path(r'^komax_tasks/(?P<task_name>[a-zA-Z0-9_.-]*)/get_task_komax/(?P<komax>\d+)/$',
            views.get_personal_task_view_komax, name='get_spec_task'),
    re_path(r'^komax_tasks/(?P<task_name>[a-zA-Z0-9_.-]*)/get_task_kappa/(?P<kappa>\d+)/$',
            views.get_personal_task_view_kappa, name='get_spec_task_kappa'),
    re_path(r'^komax_tasks/task/(?P<task_name>[a-zA-Z0-9_.-]*)/get_ticket_komax/(?P<komax>\d+)/$',
            views.get_komax_ticket_view, name='get_ticket_view'),
    re_path(r'^komax_tasks/task/(?P<task_name>[a-zA-Z0-9_.-]*)/get_ticket_kappa/(?P<kappa>\d+)/$',
            views.get_kappa_ticket_view, name='get_kappa_ticket_view'),
    re_path(r'^json/test/get/harness/(?P<harness_number>\d+[\w-]+)$', views.handle_json_get, name='json_test_get_harness'),
    re_path(r'^json/test/post/$', views.handle_json_post, name='json_test_post'),
    re_path(r'^json/task_personal/(?P<identifier>[A-Z]*)/$', views.TaskPersonalJsonView.as_view(), name='task_personal_view'),
    re_path(r'^harnesses/$', views.HarnessesListView.as_view(), name='harnesses'),
    # re_path(r'^harnesses/upload/$', views.upload_temp_chart, name='temp_chart_upload'),
    path('harnesses/<harness_number>/delete/', views.harness_delete, name='delete_harness'),
    path('harnesses/<harness_number>/download/', views.get_harness_chart_view, name='download_harness'),
    re_path(r'^komaxes/$', views.EquipmentListView.as_view(), name='komaxes'),
    # re_path(r'^komaxes/edit/(?P<pk>\d+)/$', views.KomaxEditView.as_view(), name='komaxes_edit'),
    path('harnesses/<harness_number>', views.harness_chart_view, name='harness_chart'),
    re_path(r'^laboriousness/$', views.LaboriousnessListView.as_view(), name='laboriousness'),
    re_path(r'^komax_tasks/$', views.KomaxTaskListView.as_view(), name='komax_task_list'),
    re_path(r'^komax_terminals/$', views.KomaxTerminalsListView.as_view(), name='komax_terminals_list'),
    re_path(r'^komax_tasks/task/(?P<task_name>[a-zA-Z0-9_.-]*)/load_task/$', views.load_task, name='load_komax_task')
    #path('upload/', views.upload, name='upload'),
]