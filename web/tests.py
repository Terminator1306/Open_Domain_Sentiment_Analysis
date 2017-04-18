# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from models import *
# Create your tests here.
brand = [url.brand for url in Url.objects.get(platform='tm')]
print brand