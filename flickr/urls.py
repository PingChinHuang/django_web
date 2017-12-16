"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url
from flickr import views
#from django.contrib import admin

urlpatterns = [
    #url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^photosets/$', views.photosets, name='photosets'),
    url(r'^photosets/page/(?P<page>[0-9]+)/$', views.photosets, name='photosets'),
    url(r'^photoset/(?P<setid>[0-9]+)/(?P<page>[0-9]+)/$', views.photoset, name='photoset'),
    url(r'^photo/(?P<photoid>[0-9]+)/tags/add$', views.photo_tags_add, name='photo_tags_add'),
    url(r'^photo/(?P<photoid>[0-9]+)/tags/get$', views.photo_tags_get, name='photo_tags_get'),
    url(r'^photo/(?P<photoid>[0-9]+)/tags/remove$', views.photo_tags_remove, name='photo_tags_remove'),
]
