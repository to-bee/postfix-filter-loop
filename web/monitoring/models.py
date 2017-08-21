from abc import abstractmethod
import datetime
import os
from abc import abstractmethod
from enum import Enum
from django.utils.dateparse import parse_datetime

import numpy as np
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils import timezone, formats

from django.db import models

class BaseComponent(models.Model):
    class Meta:
        abstract = True
        # must be managed - otherwise tables won't be generated
        managed = True

    @abstractmethod
    def __str__(self):
        pass

    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=timezone.now, null=True, editable=False)
    modified = models.DateTimeField(auto_now=timezone.now, null=True, editable=False)

    # @property
    # def modified_formated(self):
    #     return formats.date_format(self.modified, "SHORT_DATETIME_FORMAT")

class Email(BaseComponent):
    def __str__(self):
        origin_information = '%s -> %s' % (self.sender, self.recipient)
        return '<%s> | %s' % (origin_information, self.subject) if self.subject is not None else origin_information

    sender = models.CharField(null=False, blank=False, max_length=255)
    recipient = models.CharField(null=True, blank=True, max_length=255)
    content_type = models.CharField(null=True, blank=True, max_length=255)
    reply_to = models.CharField(null=True, blank=True, max_length=255)
    mime_version = models.CharField(null=True, blank=True, max_length=255)
    message_id = models.CharField(null=True, blank=True, max_length=255)
    received = models.CharField(null=True, blank=True, max_length=255)
    references = models.CharField(null=True, blank=True, max_length=255)
    user_agent = models.CharField(null=True, blank=True, max_length=255)
    x_sender = models.CharField(null=True, blank=True, max_length=255)
    subject = models.CharField(null=True, blank=True, max_length=255)
    body = models.TextField(null=True, blank=True)
    x_virus_scanned = models.BooleanField(null=False, default=False)