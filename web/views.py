# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import logging
from django.http import HttpResponse

from django.shortcuts import render
from sentiment_analysor import sentiment
from django.core import serializers
from models import *
import os


def crawler(request):
    category = NameKey.objects.values("name").filter(type='category').order_by("id")
    platform = NameKey.objects.values("name").filter(type='platform').order_by("id")
    brand = Url.objects.filter(platform='tm', category='phone')
    return render(request, "crawler.html", locals())


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
    platform = NameKey.objects.get(name=data['platform']).key
    category = NameKey.objects.get(name=data['cat']).key
    brand = Url.objects.filter(platform=platform, category=category)
    return HttpResponse(serializers.serialize("json", brand))


def crawl_comment(request):
    data = request.GET
    platform = NameKey.objects.get(name=data['platform']).key
    category = NameKey.objects.get(name=data['cat']).key
    brand = data['brand']
    brand_id = Url.objects.get(platform=platform, category=category, brand=brand).id
    command = "run_crawler.bat %s %d" % (platform, brand_id)
    os.system(command)
    return HttpResponse(json.dumps({"command": command}))
