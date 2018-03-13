from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver

from rest.apps.core.api.serializers.search import *
from rest.apps.core.models import User
from rest.apps.core.search_indexes import UserIndex

@receiver(post_save, sender=User, dispatch_uid="update_user_index")
def update_es_user_record(sender, instance, **kwargs):
    obj = UserElasticSerializer(instance)
    obj.save()


@receiver(post_delete, sender=User, dispatch_uid="delete_user_index")
def delete_es_user_record(sender, instance, *args, **kwargs):
    obj = UserElasticSerializer(instance)
    obj.delete(ignore=404)
