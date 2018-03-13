from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch_dsl import DocType, Integer, Text, Date, Keyword


class UserIndex(DocType):
    pk = Integer()
    username = Text(fields={'raw': Keyword()})
    date_joined = Date()

    class Meta:
        index = 'user'
