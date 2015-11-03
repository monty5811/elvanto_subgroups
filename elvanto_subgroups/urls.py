# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework.permissions import IsAuthenticated

from elvanto_subgroups import views_api as va
from elvanto_subgroups import views
from elvanto_subgroups.models import Link
from elvanto_subgroups.serializers import LinkSerializer

admin.autodiscover()

urls_basic = [
    url(r'^admin/', include(admin.site.urls)),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'link/add/$', views.LinkCreate.as_view(), name='link_add'),
    url(r'link/(?P<pk>[0-9]+)/$', views.LinkUpdate.as_view(), name='link_update'),
    url(r'link/(?P<pk>[0-9]+)/delete/$', views.LinkDelete.as_view(), name='link_delete'),
]
urls_api = [
    # api
    url(r'^api/v1/elvanto/links/$',
        va.ApiCollection.as_view(model_class=Link,
                                 serializer_class=LinkSerializer,
                                 permission_classes=(IsAuthenticated,)
                                 ),
        name='api_links'),
]

urlpatterns = urls_basic + urls_api
