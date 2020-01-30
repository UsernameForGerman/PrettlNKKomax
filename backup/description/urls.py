from django.urls import path, re_path
from django.views.generic import TemplateView

app_name = 'description'
urlpatterns = [
    re_path(r'^$', TemplateView.as_view(template_name='description/description.html'), name='description'),
]