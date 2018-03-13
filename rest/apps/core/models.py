"""
(C) 2016 - Laszlo Marai <atleta@atleta.hu>
"""
import re
import uuid
from functools import update_wrapper

from django.contrib.auth.base_user import BaseUserManager
from django.contrib .auth.models import (AbstractBaseUser, PermissionsMixin)
from django.core import validators
from django.db import models
from django.utils import timezone
from django.utils.deconstruct import deconstructible
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices
from six import wraps

@deconstructible
class UploadDir:
    def __init__(self, path):
        self.path = path

    def __call__(self, instance, filename):
      return "%s/%s.%s" % (self.path, uuid.uuid4(), filename.split('.')[-1])


def get_file_path():
    pass

from rest.apps.core.search_indexes import UserIndex


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, **kwargs):
        """
        Creates and saves a User with the given email and password.
        """
        if not kwargs.get(self.model.USERNAME_FIELD, None):
            raise ValueError('The USERNAME_FIELD (%s) must be provided' % self.model.USERNAME_FIELD)

        # TODO: clean this up and make generic. Why is username normalized by the model and email by the manager?
        for k, v in kwargs.items():
            method_name = 'normalize_%s' % k
            normalizer = getattr(self, method_name, getattr(self.model, method_name, None))
            if normalizer:
                kwargs[k] = normalizer(v)

        password = kwargs.pop('password')
        user = self.model(**kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, **kwargs):
        kwargs.setdefault('is_superuser', False)
        return self._create_user(**kwargs)

    def create_superuser(self, **kwargs):
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_staff', True)

        return self._create_user(**kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    GENDER = (
        ('male', 'Male'),
        ('female', 'Female'),
    )

    email = models.EmailField(_('email address'), unique=True, db_index=True, validators=[validators.EmailValidator()])

    username = models.CharField(_('username'), max_length=30, unique=True,
                               validators=[
                                   validators.RegexValidator(re.compile('^[\w.+-]+$'),
                                                             _('Enter a valid username.'),
                                                             'invalid')
                               ])

    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_(
                                       'Designates whether the user can log into this admin '
                                       'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_(
                                        'Designates whether this user should be treated as '
                                        'active. Unselect this instead of deleting accounts.'))
    photo = models.FileField(blank=True, upload_to='photo')
    gender = models.CharField(max_length=6, choices=GENDER)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.username)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        return '%s %s' % (self.first_name, self.last_name)

    def indexing(self):
        obj = UserIndex(
            meta={'pk': self.pk},
            username=self.username,
            date_joined=self.date_joined
        )
        obj.save()
        return obj.to_dict(include_meta=True)
