"""YXSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from django.urls import path, include, re_path

from django.urls import path, include, re_path
from .views import page

urlpatterns = [
    re_path(r'^(?P<slug>[\w./-]+)/$', page, name='page'),
    re_path(r'^$', page, name='homepage'),
    #path('doc', doc),
    #re_path(r'^image/(?P<width>[0-9]+)x(?P<height>[0-9]+)/$', image_placeholder, name='placeholder'),
    #re_path(r'^.*$', doc),
]