# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone


class ModelManager(models.Manager):
    use_for_related_fields = True

    def get_queryset(self):
        return super(ModelManager, self).get_queryset().filter(is_active=True, is_deleted=False)

    def all(self, *args, **kwargs):
        return super(ModelManager, self).filter(is_active=True, is_deleted=False)

    def filter(self, *args, **kwargs):
        return super(ModelManager, self).filter(is_active=True, is_deleted=False).filter(*args, **kwargs)

    def get(self, *args, **kwargs):
        return super(ModelManager, self).filter(is_active=True, is_deleted=False).filter(*args, **kwargs)

    def active(self, *args, **kwargs):
        return super(ModelManager, self).filter(is_active=True, is_deleted=False)
