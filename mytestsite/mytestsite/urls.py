"""mytestsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path,re_path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import staticfiles

urlpatterns = [
    #path('', views.decrypt),
    re_path(r'c(.+)k(.+)/$', views.decrypt),
    path('',views.encrypt),
    path('api/qrcode',views.qrcode_making),
    #path('api/encryptK',views.encryptK),
    path('api/encryptC',views.encryption),
    path('api/encryptK',views.encryptionK),
    path('api/decryptC',views.decryptC),
]

urlpatterns += staticfiles_urlpatterns()
