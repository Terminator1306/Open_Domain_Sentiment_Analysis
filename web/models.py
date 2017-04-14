# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Product(models.Model):
    product_id = models.CharField(primary_key=True)
    comment_count = models.CharField()
    brand = models.CharField()
    model = models.CharField()
    price = models.CharField()
    name = models.CharField()
    category = models.CharField()
    commentTag = models.TextField()
    attribute = models.TextField()


class Comment(models.Model):
    product_id = models.CharField()
    comment_id = models.CharField()
    referenceName = models.CharField()
    creationTime = models.CharField()
    content = models.TextField()
    attribute = models.TextField()

    class Meta:
        unique_together("product_id", "comment_id")
