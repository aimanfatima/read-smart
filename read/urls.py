"""read URL Configuration

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
from django.urls import path, include
from pdfreader import urls as pdfreader_urls
from quesgenerator import urls as quesgenerator_urls
from docreader import urls as docreader_urls
from homepage import urls as homepage_urls
from linkreader import urls as linkreader_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include((homepage_urls, "homepage_urls"))),
    path("", include((pdfreader_urls, "pdfreader_urls"))),
    path("", include((quesgenerator_urls, "quesgenerator_urls"))),
    path("", include((docreader_urls, "docreader_urls"))),
    path("", include((linkreader_urls, "linkreader_urls")))
]
