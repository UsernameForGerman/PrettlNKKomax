from django.contrib import admin
from django.urls import path, include, re_path
from . import views
from django.views.generic import TemplateView

app_name = 'komax_app'

urlpatterns = [
    path('', views.MainPageKomaxAppView.as_view(), name='komax_app_view'),
    path('api/v1/komax/', views.KomaxClientView.as_view(), name='komax_client'),
    path('tasks/', views.TasksView.as_view(), name='tasks_view'),
    path('account/', views.WorkerAccountView.as_view(), name='user_account'),
    path('tasks/setup/', views.KomaxTaskSetupView.as_view(), name='task_setup'),
    path('tasks/<str:task_name>/', views.KomaxTaskView.as_view(), name='task_view'),
    path('tasks/<str:task_name>/delete/', views.delete_task, name='delete_task'),
    path('tasks/<str:task_name>/get_task/', views.get_general_task_view, name='get_task'),
    path('tasks/<str:task_name>/get_tech_task/', views.get_general_tech_task_view, name='get_tech_task'),
    path('tasks/<str:task_name>/get_task_komax/<str:komax>/',
            views.get_personal_task_view_komax, name='get_spec_task'),
    path('tasks/<str:task_name>/get_task_kappa/<str:kappa>/',
            views.get_personal_task_view_kappa, name='get_spec_task_kappa'),
    path('tasks/<str:task_name>/get_ticket_komax/<str:komax>/',
            views.get_komax_ticket_view, name='get_ticket_view'),
    path('tasks/<str:task_name>/get_ticket_kappa/<str:kappa>/',
            views.get_kappa_ticket_view, name='get_kappa_ticket_view'),
    path('tasks/<str:task_name>/send_task/', views.send_task_to_worker,
                name='send_komax_task'),
    path('tasks/<task_name>/load_task/', views.load_task_to_komax, name='load_komax_task'),

    # harnesses
    path('harnesses/', views.HarnessesListView.as_view(), name='harnesses'),
    path('harnesses/<str:harness_number>', views.harness_chart_view, name='harness_chart'),
    path('harnesses/<str:harness_number>/delete/', views.harness_delete, name='delete_harness'),
    path('harnesses/<str:harness_number>/download/', views.get_harness_chart_view, name='download_harness'),

    # others
    # re_path(r'^harnesses/upload/$', views.upload_temp_chart, name='temp_chart_upload'),
    path('komaxes/', views.EquipmentListView.as_view(), name='komaxes'),


    # re_path(r'^komaxes/edit/(?P<pk>\d+)/$', views.KomaxEditView.as_view(), name='komaxes_edit'),
    path('laboriousness/', views.LaboriousnessListView.as_view(), name='laboriousness'),
    path('komax_tasks/', views.KomaxTaskListView.as_view(), name='komax_task_list'),
    path('komax_terminals/', views.KomaxTerminalsListView.as_view(), name='komax_terminals_list'),


    #re_path(r'^komax_tasks/(?P<task_name>[a-zA-Z0-9_.-]*)/$', views.KomaxTaskView.as_view(), name='task_view'),
    #re_path(r'^setup/$', views.KomaxAppSetupView.as_view(), name='task_setup'),
    #re_path(r'^komax_tasks/(?P<pk>\d+[\w-]+)/amount/$', views.set_amount_task_view, name='task_amount'),
    #re_path(r'^komax_tasks/(?P<task_name>[a-zA-Z0-9_.-]*)/get_task/$', views.get_general_task_view, name='get_task'),
    #re_path(r'^komax_tasks/(?P<task_name>[a-zA-Z0-9_.-]*)/get_tech_task$', views.get_general_tech_task_view, name='get_tech_task'),
    #re_path(r'^komax_tasks/(?P<task_name>[a-zA-Z0-9_.-]*)/get_task_komax/(?P<komax>\d+)/$',
    #        views.get_personal_task_view_komax, name='get_spec_task'),
    #re_path(r'^komax_tasks/(?P<task_name>[a-zA-Z0-9_.-]*)/get_task_kappa/(?P<kappa>\d+)/$',
    #        views.get_personal_task_view_kappa, name='get_spec_task_kappa'),
    #re_path(r'^komax_tasks/task/(?P<task_name>[a-zA-Z0-9_.-]*)/get_ticket_komax/(?P<komax>\d+)/$',
    #        views.get_komax_ticket_view, name='get_ticket_view'),
    #re_path(r'^komax_tasks/task/(?P<task_name>[a-zA-Z0-9_.-]*)/get_ticket_kappa/(?P<kappa>\d+)/$',
    #        views.get_kappa_ticket_view, name='get_kappa_ticket_view'),
    #re_path(r'^json/test/get/harness/(?P<harness_number>\d+[\w-]+)$', views.handle_json_get, name='json_test_get_harness'),
    #re_path(r'^json/test/post/$', views.handle_json_post, name='json_test_post'),
    #re_path(r'^json/task_personal/(?P<identifier>[A-Z]*)/$', views.TaskPersonalJsonView.as_view(), name='task_personal_view'),
    #path('upload/', views.upload, name='upload'),
]
