# django libs
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# project libs
from .views import PositionInfoView, KomaxTaskPersonalView

app_name = 'komax_api'

router = DefaultRouter()

urlpatterns = [
    path('v1/position/', PositionInfoView.as_view(), name='position-view'),
    path('v1/komax_task_personal/', KomaxTaskPersonalView.as_view(), name='komax-task-personal'),
    path('v1/', include(router.urls)),
]