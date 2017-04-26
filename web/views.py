# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import logging
from django.http import HttpResponse
from django.http import HttpRequest

from django.shortcuts import render
from sentiment_analysor import sentiment
from django.core import serializers
from models import *
import os
from db import dbconnect
import time

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger('mylogger')

db = dbconnect.connect()

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


def get_brand_list(request):
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
    # os.system(command)

    output_file = platform + '_' + category + '_' + str(brand_id) + '.sql'
    output_file = "D:/Yan/gp/gp_web/db_output/" + output_file
    if os.path.exists(output_file):
        os.remove(output_file)
    c = db.cursor()
    c.execute("set names utf8")
    sql = "select web_product.product_id, comment_id, referenceName, creationTime, content, web_comment.attribute" \
          " from web_comment, web_product where web_comment.product_id = web_product.product_id and category = '%s'" \
          " and web_comment.product_id like '%s_%%' and brand = '%s' into outfile '%s' character set gbk " \
          % (category, platform.upper(), data['brand'], output_file)
    c.execute(str(sql))
    return HttpResponse(json.dumps({"output_file": output_file}))


def get_product_list(request):
    data = request.GET
    platform = NameKey.objects.get(name=data['platform']).key
    category = NameKey.objects.get(name=data['cat']).key
    products = Product.objects.filter(category=category, brand=data['brand'], product_id__startswith=platform.upper())
    return HttpResponse(serializers.serialize("json", products))


def download_comment(request):
    data = request.GET
    platform = NameKey.objects.get(name=data['platform']).key
    category = NameKey.objects.get(name=data['cat']).key
    brand_id = Url.objects.get(platform=platform, category=category, brand=data['brand']).id
    file_name = platform + '_' + category + '_' + str(brand_id) + '.sql'
    file_name = 'D:/Yan/gp/gp_web/db_output/' + file_name
    return HttpRequest()
