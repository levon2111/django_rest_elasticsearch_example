#!/usr/bin/env python
# coding=utf-8

from django.conf import settings

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from elasticsearch import Elasticsearch, RequestsHttpConnection
from rest_framework_elasticsearch import es_views, es_pagination, es_filters

from rest.apps.core.search_indexes import UserIndex

class SearchFilter(es_filters.ElasticSearchFilter):
    search_param = 'q'


filter_backends = (
    es_filters.ElasticFieldsFilter,
    SearchFilter
)


class UserSearchView(es_views.ListElasticAPIView):
    es_client = Elasticsearch(hosts=[settings.ELASTIC_URL], connection_class=RequestsHttpConnection)
    es_model = UserIndex
    es_filter_backends = filter_backends
    es_search_fields = ('username', )

SEARCH_VIEWS = {
    'users': UserSearchView.as_view()
}


class SearchAPIView(APIView):
    def get(self, request, *args, **kwargs):
        topic = request.GET.get('topic')

        if not topic:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'detail': 'topic not found'})

        return SEARCH_VIEWS[topic](self.request._request, *args, **kwargs)
