# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Product(models.Model):
    product_id = models.CharField(max_length=254, primary_key=True)
    comment_count = models.CharField(max_length=254, default='')
    url = models.TextField(default='')
    brand = models.CharField(max_length=254, default='')
    model = models.CharField(max_length=254, default='')
    price = models.CharField(max_length=254, default='')
    name = models.CharField(max_length=254, default='')
    category = models.CharField(max_length=254, default='')
    commentTag = models.TextField()
    attribute = models.TextField()


class Comment(models.Model):
    product_id = models.CharField(max_length=255, default='')
    comment_id = models.CharField(max_length=254)
    referenceName = models.CharField(max_length=254, default='')
    creationTime = models.CharField(max_length=254, default='')
    content = models.TextField()
    attribute = models.TextField()
    sentiment = models.TextField(null=True)

    class Meta:
        unique_together = ("product_id", "comment_id")


class Url(models.Model):
    category = models.CharField(max_length=255,default='')
    brand = models.CharField(max_length=255, default='')
    platform = models.CharField(max_length=255, default='')
    url = models.CharField(max_length=255, unique=True)


class NameKey(models.Model):
    name = models.CharField(max_length=255, default='')
    key = models.CharField(max_length=255)
    type = models.CharField(max_length=255, default='')
