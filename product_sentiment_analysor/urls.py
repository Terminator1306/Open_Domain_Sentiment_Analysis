"""product_sentiment_analysor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from web import views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^crawler/$', views.crawler, name='crawler'),
    url(r'^sentiment_product/$', views.sentiment_product, name='sentiment_product'),
    url(r'^sentiment_comment/$', views.sentiment_comment, name='sentiment_comment'),
    url(r'^sentiment_brand/$', views.sentiment_brand, name='sentiment_brand'),
    url(r'^sentiment_comment/compute/comment/$', views.compute_sentiment_comment, name='compute_comment'),
    url(r'^$', views.home, name='home'),
    url(r'^get_brand/$', views.get_brand_list, name="get_brand"),
    url(r'get_product', views.get_product_list, name='get_product'),
    url(r'^crawl_comment/$', views.crawl_comment, name='crawl_comment'),
]
