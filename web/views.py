# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import logging
from django.http import HttpResponse

from django.shortcuts import render
from sentiment_analysor import sentiment
from models import *


def crawler(request):
    category = ["手机", "笔记本"]
    platform = ["天猫", "京东"]
    brand = Url.objects.filter(platform='tm', category='phone')
    return render(request, "crawler.html", {"brand": brand, "category": category, "platform": platform})


def home(request):
    return render(request, "home.html")


def sentiment_comment(request):
    category = ["手机", "笔记本"]
    return render(request, "sentiment_comment.html", {"category": category})


def sentiment_product(request):
    category = ["手机", "笔记本"]
    platform = ["天猫", "京东"]
    brand = Url.objects.filter(platform='tm', category='phone')
    product = []
    return render(request, "sentiment_product.html", {"brand": brand, "category": category, "platform": platform})


def sentiment_brand(request):
    category = ["手机", "笔记本"]
    platform = ["天猫", "京东"]
    brand = Url.objects.filter(platform='tm', category='phone')
    return render(request, "sentiment_brand.html", {"brand": brand, "category": category, "platform": platform})


def compute_sentiment_comment(request):
    data = request.GET
    sentiment_result = sentiment.compute_sentiment(data['comment'])
    result = {'aspect': sentiment_result.keys(),
              'value': [sentiment_result[aspect] for aspect in sentiment_result.keys()]}
    return HttpResponse(json.dumps(result))
