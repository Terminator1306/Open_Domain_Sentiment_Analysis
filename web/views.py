# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import logging
from django.http import HttpResponse

from django.shortcuts import render
from sentiment_analysor import sentiment

# Create your views here.
# logger = logging.getLogger('aaa')


def crawler(request):
    return render(request, "crawler.html")


def home(request):
    return render(request, "home.html")


def sentiment_comment(request):
    category = ["手机", "笔记本"]
    return render(request, "sentiment_comment.html", {"category": category, "first": category[0]})


def sentiment_product(request):
    category = ["手机", "笔记本"]
    platform = ["天猫", "淘宝"]
    brand = []
    product = []
    return render(request, "sentiment_product.html")


def sentiment_brand(request):
    return render(request, "sentiment_brand.html")


def compute_sentiment_comment(request):
    data = request.GET
    sentiment_result = sentiment.compute_sentiment(data['comment'])
    result = {'aspect': sentiment_result.keys(), 'value': [sentiment_result[aspect] for aspect in sentiment_result.keys()]}
    return HttpResponse(json.dumps(result))

