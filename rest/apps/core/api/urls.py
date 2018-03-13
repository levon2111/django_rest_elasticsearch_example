#!/usr/bin/env python
# coding=utf-8
from django.conf.urls import url
from django.urls import include
from rest_framework.routers import SimpleRouter, DefaultRouter

from rest.apps.core.api.views.search import SearchAPIView

router = DefaultRouter()
urlpatterns = [
    url('', include(router.urls)),
    url(r'^search/$', SearchAPIView.as_view()),
]
