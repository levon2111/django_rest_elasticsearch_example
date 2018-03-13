#!/usr/bin/env python
# coding=utf-8
from django.apps import AppConfig
from django.conf import settings
from django.db import ProgrammingError
from django.db.models.signals import post_save


class CoreAppConfig(AppConfig):
    name = 'rest.apps.core'
    verbose_name = 'rest'

    def ready(self):
        self.configure_sites()
        self.configure_social_apps()
        from . import signals


    def test_ready(self):
        self.ready()
