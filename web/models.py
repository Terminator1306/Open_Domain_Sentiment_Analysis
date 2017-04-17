# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Product(models.Model):
    product_id = models.CharField(max_length=254, primary_key=True)
    comment_count = models.CharField(max_length=254)
    brand = models.CharField(max_length=254)
    model = models.CharField(max_length=254)
    price = models.CharField(max_length=254)
    name = models.CharField(max_length=254)
    category = models.CharField(max_length=254)
    commentTag = models.TextField()
    attribute = models.TextField()


class Comment(models.Model):
    product_id = models.CharField(max_length=254)
    comment_id = models.CharField(max_length=254)
    referenceName = models.CharField(max_length=254)
    creationTime = models.CharField(max_length=254)
    content = models.TextField()
    attribute = models.TextField()

    class Meta:
        unique_together = ("product_id", "comment_id")
