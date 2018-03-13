from django.conf.urls import include, url
from django.contrib import admin
admin.autodiscover()

import rest.apps.core.urls
import rest.apps.auth.urls

def bad(request):
    """ Simulates a server error """
    1 / 0

urlpatterns = [
    url(r'^', include(rest.apps.core.urls)),
]

