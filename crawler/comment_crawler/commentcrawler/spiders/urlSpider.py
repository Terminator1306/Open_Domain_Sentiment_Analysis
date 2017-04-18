# coding:utf-8
import scrapy
import re
import json
import HTMLParser
from commentcrawler.items import *


class UrlSpider(scrapy.Spider):
    name = "url"
    start_urls = {
        "tm_phone": "https://list.tmall.com/search_product.htm?spm=a220m.1000858.0.0.ycmb1R&cat=50024400&q=%CA%D6%BB%FA&sort=s&style=g&search_condition=7&from=sn_1_rightnav&active=2&industryCatId=50024400#J_crumbs",
        "tm_laptop": "https://list.tmall.com/search_product.htm?spm=a220m.1000858.0.0.UOozRt&cat=50024399&q=%B1%CA%BC%C7%B1%BE&sort=s&style=g&search_condition=7&from=sn_1_rightnav&industryCatId=53354012#J_crumbs",
        "jd_phone": "https://search.jd.com/search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&offset=3&wq=%E6%89%8B%E6%9C%BA&cid3=655#J_searchWrap",
        "jd_laptop": "https://search.jd.com/search?keyword=%E7%AC%94%E8%AE%B0%E6%9C%AC&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&offset=3&cid3=672#J_searchWrap"
    }

    cookies = {
        'cna': 'MgGQDlZ+nHsCAWonKbYoFjaM',
        '_med': 'dw:1440&dh:900&pw:1440&ph:900&ist:0',
        't': '265651046d436fb6c5a7a398e4d65a4c',
        '_tb_token_': 'oIA8dqMGpOuU',
        'cookie2': '1abd1988561b207bbffbc860ebcbeb2f',
        'pnm_cku822': '075UW5TcyMNYQwiAiwQRHhBfEF8QXtHcklnMWc%3D%7CUm5OcktwRX5FeEF5THNNciQ%3D%7CU2xMHDJ7G2AHYg8hAS8WIgwsAl4%2FWTVSLFZ4Lng%3D%7CVGhXd1llXGdSaVJvVm5bZFplUm9NdEl3SXdPc0l9RXhEcUR9R2k%2F%7CVWldfS0TMwY4BycSMhwkFHMIWDVfe1UDVQ%3D%3D%7CVmhIGCUFOQc8BycbIh0jAzgFPAIiHiceIwM3CjcXKxIrFjYDOAVTBQ%3D%3D%7CV25Tbk5zU2xMcEl1VWtTaUlwJg%3D%3D',
        'res': 'scroll%3A1423*6043-client%3A1423*799-offset%3A1423*6043-screen%3A1440*900',
        'cq': 'ccp%3D1',
        'l': 'AoCAedPj4WQcxKerV6ErAiSI0ARSCWTT',
        'isg': 'AikpBI00WtENd2aQhdgdXB8vONXKrB0oyAa8HMsepZBPkkmkE0Yt-BeAIoFe'
    }

    allowed_domains = ["tmall.com", "jd.com", "3.cn", "jd.hk"]

    def start_requests(self):
        for k, v in self.start_urls.items():
            info = k.split('_')
            platform = info[0]
            cat = info[1]
            if platform == 'tm':
                yield scrapy.Request(v, cookies=self.cookies, callback=self.tm_parse, dont_filter=True,
                                     meta={'cat': cat})
            else:
                yield scrapy.Request(v, callback=self.jd_parse, dont_filter=True, meta={'cat': cat})

    def tm_parse(self, response):
        head = "https://list.tmall.com/search_product.htm"
        sel = scrapy.Selector(response)
        url_ul = sel.xpath("//div[@class='attrValues showLogo']/ul/li")
        for li in url_ul:
            url = head + li.xpath("./a/@href").extract()[0]
            brand = li.xpath("./a/@title").extract()[0]
            url_item = Url()
            url_item['url'] = url
            url_item['brand'] = brand
            url_item['platform'] = 'tm'
            url_item['category'] = response.meta['cat']
            url_item['item_type'] = 'url'
            yield url_item

    def jd_parse(self, response):
        head = "https://search.jd.com/"
        sel = scrapy.Selector(response)
        url_ul = sel.xpath("//ul[@class='J_valueList v-fixed']/li")
        for li in url_ul:
            url = head + li.xpath("./a/@href").extract()[0]
            brand = li.xpath("./a/@title").extract()[0]
            url_item = Url()
            url_item['url'] = url
            url_item['brand'] = brand
            url_item['platform'] = 'jd'
            url_item['category'] = response.meta['cat']
            url_item['item_type'] = 'url'
            yield url_item
