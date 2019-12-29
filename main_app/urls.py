from django.urls import path, re_path

from django.views.generic import TemplateView

app_name = 'main_app'
urlpatterns = [
    re_path(r'^$', TemplateView.as_view(template_name='main_app/welcome.html'), name='main_app'),
]