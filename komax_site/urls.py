"""komax_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include, re_path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from komax_app import views


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    # path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    # re_path(r'^', include('main_app.urls')),
    # path('', include('komax_app.urls')),
    path('api/', include('api_komax_app.urls')),
    # re_path(r'^description/', include('description.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    re_path(r'^.*$', views.index),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""
urlpatterns += i18n_patterns(
    re_path(r'^', include('main_app.urls')),
    re_path(r'^komax_app/', include('komax_app.urls')),
    re_path(r'^description/', include('description.urls')),
)
"""

