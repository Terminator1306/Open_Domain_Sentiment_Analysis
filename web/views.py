# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import logging
from django.http import HttpResponse

from django.shortcuts import render
from sentiment_analysor import sentiment
from models import *


def crawler(request):
    category = NameKey.objects.values("name").filter(type='category').order_by("id")
    platform = NameKey.objects.values("name").filter(type='platform').order_by("id")
    brand = Url.objects.filter(platform='tm', category='phone').order_by("id")
    return render(request, "crawler.html", {"brand": brand, "category": category, "platform": platform})


def home(request):
    return render(request, "home.html")


def sentiment_comment(request):
    category = NameKey.objects.values("name").filter(type='category').order_by("id")
    return render(request, "sentiment_comment.html", locals())


def sentiment_product(request):
    category = NameKey.objects.values("name").filter(type='category').order_by("id")
    platform = NameKey.objects.values("name").filter(type='platform').order_by("id")
    brand = Url.objects.filter(platform='tm', category='phone')
    product = []
    return render(request, "sentiment_product.html", locals())


def sentiment_brand(request):
    category = NameKey.objects.values("name").filter(type='category').order_by("id")
    platform = NameKey.objects.values("name").filter(type='platform').order_by("id")
    brand = Url.objects.filter(platform='tm', category='phone')
    return render(request, "sentiment_brand.html", locals())


def compute_sentiment_comment(request):
    data = request.GET
    sentiment_result = sentiment.compute_sentiment(data['comment'])
    result = {'aspect': sentiment_result.keys(),
              'value': [sentiment_result[aspect] for aspect in sentiment_result.keys()]}
    return HttpResponse(json.dumps(result))


def get_brand_by_cat(request):
    data = request.GET
    brand = Url.objects.filter(platform=NameKey.objects.get(name=data.platform),
                               category=NameKey.objects.get(name=data.cat))
    return HttpResponse(json.dumps(brand))
