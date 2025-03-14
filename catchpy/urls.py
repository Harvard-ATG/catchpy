"""catch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import include
from django.urls import path
from django.urls import re_path
from django.contrib import admin

from . import views

# import these when adding catchpy to an existing django project
urls = [
    re_path(r'^annos/?', include('catchpy.anno.urls')),
    path('version', views.app_version),
    path('is_alive', views.is_alive),
]
# urlpatterns = urls + [path('admin/', admin.site.urls)]x
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(urls)),
]
