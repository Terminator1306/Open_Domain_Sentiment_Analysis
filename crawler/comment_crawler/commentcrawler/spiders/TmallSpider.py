# coding:utf-8
import scrapy
import re
import json
import HTMLParser
from commentcrawler.items import *
import MySQLdb


class TmallSpider(scrapy.Spider):
    name = "tm"
    pages = 0
    maxpage = 10
    allowed_domains = ["tmall.com"]

    start = []
    cookies ={
        'x': '__ll%3D-1%26_ato%3D0',
        '_med': 'dw:1366&dh:768&pw:1366&ph:768&ist:0',
        'tk_trace': '1',
         '_tb_token_': 'Ur4N5kpuIRQY',
         'uc1': 'cookie15=URm48syIIVrSKA%3D%3D&existShop=false',
         'uc3': 'nk2=gKRAFy4%3D&id2=VWolk1ZEqVZ%2B&vt3=F8dARVKyod1F26sWbEE%3D&lg2=V32FPkk%2Fw0dUvg%3D%3D',
         'uss': 'V3%2BObjrWeiX%2FdUgjAhJ0EucHdfYLVdOtNip8w7Rz%2F9aJW%2Fo4VUEvCKRH',
         'lgc': '%5Cu95EB%5Cu660A1',
         'tracknick': '%5Cu95EB%5Cu660A1',
         'cookie2': 'bd8f5e9f59f4ca765adb7397bf603adc',
         'cookie1': 'VT5QjUKltzGCqDfj4XDJYpfk9QXHK0W6saPIVZCKXOc%3D',
         'unb': '654811527',
         'skt': 'ecf9e6180d8e77bd',# a
         't': 'ef41b0fbd876a14021126e8df1aa9cdb',
         '_l_g_': 'Ug%3D%3D',
         '_nk_': '%5Cu95EB%5Cu660A1',
         'cookie17': 'VWolk1ZEqVZ%2B',
         'login': 'true',
         'tt': 'login.tmall.com',
         'cna': 'EFurEFJmHUECAdvv49S5egNZ',
         'pnm_cku822': '215UW5TcyMNYQwiAiwQRHhBfEF8QXtHcklnMWc%3D%7CUm5Ockt%2FQHVOdUtySnJJdCI%3D%7CU2xMHDJ7G2AHYg8hAS8XLQMjDVEwVjpdI1l3IXc%3D%7CVGhXd1llXGhXYlliXGVdZV5jVGlLdExwT3RLd0pwTXFMcER%2BSmQy%7CVWldfS0TMwgxCioWLQ0jGCwJLF4hSDMffw4%2BGidWaEYQRg%3D%3D%7CVmhIGCUFOBgkGiMXNw86DjAQLBIpEjIIMwYmGiQfJAQ%2BATRiNA%3D%3D%7CV25Tbk5zU2xMcEl1VWtTaUlwJg%3D%3D',
         'res': 'scroll%3A1349*5893-client%3A1349*662-offset%3A1349*5893-screen%3A1366*768',
         'cq': 'ccp%3D0',
         'otherx': 'e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0',
         'swfstore': '266533',
         'whl': '-1%260%260%260',
         'l':'AtjYez6b-cpIeHR7yXsM-CxqKAxqMDxL',# a
         'isg':'AlVVgPZnoW8ZF4UTChjNXG3sZFF28glk50Lmetf6EUwbLnUgn6IZNGPsjoVi'# a
    }

    # cookies = {
    #     'cna': 'MgGQDlZ+nHsCAWonKbYoFjaM',
    #     '_med': 'dw:1440&dh:900&pw:1440&ph:900&ist:0',
    #     't': '265651046d436fb6c5a7a398e4d65a4c',
    #     '_tb_token_': 'oIA8dqMGpOuU',
    #     'cookie2': '1abd1988561b207bbffbc860ebcbeb2f',
    #     'pnm_cku822': '075UW5TcyMNYQwiAiwQRHhBfEF8QXtHcklnMWc%3D%7CUm5OcktwRX5FeEF5THNNciQ%3D%7CU2xMHDJ7G2AHYg8hAS8WIgwsAl4%2FWTVSLFZ4Lng%3D%7CVGhXd1llXGdSaVJvVm5bZFplUm9NdEl3SXdPc0l9RXhEcUR9R2k%2F%7CVWldfS0TMwY4BycSMhwkFHMIWDVfe1UDVQ%3D%3D%7CVmhIGCUFOQc8BycbIh0jAzgFPAIiHiceIwM3CjcXKxIrFjYDOAVTBQ%3D%3D%7CV25Tbk5zU2xMcEl1VWtTaUlwJg%3D%3D',
    #     'res': 'scroll%3A1423*6043-client%3A1423*799-offset%3A1423*6043-screen%3A1440*900',
    #     'cq': 'ccp%3D1',
    #     'l': 'AoCAedPj4WQcxKerV6ErAiSI0ARSCWTT',
    #     'isg': 'AikpBI00WtENd2aQhdgdXB8vONXKrB0oyAa8HMsepZBPkkmkE0Yt-BeAIoFe'
    # }

    def __init__(self, m_id=None, **kwargs):
        super(TmallSpider, self).__init__(**kwargs)
        db = MySQLdb.connect("127.0.0.1", "root", "", "gp_web")
        c = db.cursor()
        c.execute("set names utf8")
        if m_id is not None:
            c.execute("select category, brand, url from web_url where platform = 'tm' and id = %s" % m_id)
            i = c.fetchone()
            self.start.append({'cat': i[0], 'brand': i[1], 'url': i[2]})
        else:
            c.execute("select category, brand, url from web_url where platform = 'tm'")
            for i in c.fetchall():
                self.start.append({'cat': i[0], 'brand': i[1], 'url': i[2]})
        db.close()

    def start_requests(self):
        for item in self.start:
            yield scrapy.Request(item['url'], callback=self.parse, cookies=self.cookies,
                                 meta={'cat': item['cat'], 'page': 1, 'brand': item['brand']})

    def parse(self, response):
        sel = scrapy.Selector(response)
        items = sel.xpath('//div[@class="product  "]')
        next_page = sel.xpath('//a[@class="ui-page-next"]/@href').extract()
        self.pages += 1
        for item in items:
            # item = items[0]
            product_id = "TM_" + item.xpath("@data-id").extract()[0]
            url = "https:" + item.xpath(".//div[@class='productImg-wrap']/a/@href").extract()[0]
            price = item.xpath(".//p[@class='productPrice']/em/@title").extract()[0]
            yield scrapy.Request(
                url="https://dsr-rate.tmall.com/list_dsr_info.htm?itemId=%s" % (product_id[3:],),
                meta={'price': price, 'product_id': product_id, 'url': url, 'cat': response.meta['cat'],
                      'brand': response.meta['brand']},
                cookies=self.cookies,
                callback=self.CommentCountParse
            )
        if len(next_page) > 0 and self.pages < self.maxpage:
            yield scrapy.Request(
                url="https://list.tmall.com/search_product.htm" + next_page[0],
                callback=self.parse,
                cookies=self.cookies,
                meta={'cat': response.meta['cat'], 'brand': response.meta['brand']}
            )

    def CommentCountParse(self, response):
        sel = scrapy.Selector(response)
        body = sel.xpath("//body//text()").extract()[0]
        mjson = json.loads(body[9:-1])
        yield scrapy.Request(
            url="https://rate.tmall.com/listTagClouds.htm?itemId=%s" % (response.meta['product_id'][3:],),
            meta={'price': response.meta['price'], 'product_id': response.meta['product_id'],
                  'url': response.meta['url'],
                  'gradeAvg': mjson['dsr']['gradeAvg'], 'comment_count': mjson['dsr']['rateTotal'],
                  'cat': response.meta['cat'],
                  'brand': response.meta['brand']},
            cookies=self.cookies,
            callback=self.CommentTagParse
        )

    def CommentTagParse(self, response):
        sel = scrapy.Selector(response)
        body = '{' + sel.xpath("//body//text()").extract()[0] + "}"
        mjson = json.loads(body)
        commentTag = {}
        for tag in mjson['tags']['tagClouds']:
            commentTag[tag['tag']] = tag['count']
        yield scrapy.Request(
            url=response.meta['url'],
            meta={'price': response.meta['price'], 'product_id': response.meta['product_id'], 'commentTag': commentTag,
                  'gradeAvg': response.meta['gradeAvg'], 'comment_count': response.meta['comment_count'],
                  'cat': response.meta['cat'], 'url': response.meta['url'], 'brand': response.meta['brand']},
            cookies=self.cookies,
            callback=self.ProductParse
        )

    def ProductParse(self, response):

        sel = scrapy.Selector(response)
        body = sel.xpath("//body").extract()[0]
        detail = sel.xpath("//div[@id='J_Attrs']/table[1]/tbody")
        product_id = response.meta["product_id"]
        attribute = {'gradeAvg': response.meta['gradeAvg']}
        info = re.sub("[\\n ]", "", sel.xpath("//div[@class='tm-clear']/script").extract()[-1])
        model = ""
        # brand = re.sub(".*\"brand\":\"(.*?)\"[,\\}].*", '\\1', info)
        brand = response.meta['brand']
        html_parser = HTMLParser.HTMLParser()
        brand = html_parser.unescape(brand)
        if len(brand) > 100:
            brand = ""
        name = sel.xpath("//meta[@name='keywords']/@content").extract()[0]
        if len(detail) > 0:
            keys = detail.xpath("./tr[not(@class)]/th/text()").extract()
            values = detail.xpath("./tr[not(@class)]/td/text()").extract()
            for index, key in enumerate(keys):
                attribute[key] = values[index]
                if re.compile(u".*型号").match(key):
                    model = values[index]
        product = Product()
        product['comment_count'] = response.meta['comment_count']
        product['item_type'] = "product"
        product['price'] = response.meta["price"]
        product['name'] = name
        product['url'] = str(response.meta['url'])
        product['product_id'] = product_id
        product['brand'] = brand
        product['model'] = model
        product['attribute'] = attribute
        product['commentTag'] = response.meta['commentTag']
        product['category'] = response.meta['cat']

        yield product

        limit = 150
        pages = int(response.meta['comment_count']) / 20 + 1
        if pages > limit:
            pages = limit
        for i in range(1, pages):
            yield scrapy.Request(
                url="https://rate.tmall.com/list_detail_rate.htm?itemId=%s&sellerId=1&order=3&currentPage=%d" % (
                    product_id[3:], i),
                meta={'product_id': response.meta['product_id'], 'page': i},
                cookies=self.cookies,
                callback=self.CommentParse
            )

    def CommentParse(self, response):
        sel = scrapy.Selector(response)
        body1 = sel.xpath("//body//text()").extract()[0]
        a = re.compile(r'"reply":""[^},]+"+,', re.S)
        body = a.sub(r'', body1)
        if body[-1] == '"':
            mstr = "{" + body + '"}]}}'
        else:
            mstr = "{" + body + "}"
        try:
            mjson = json.loads(mstr)
            for rate in mjson["rateDetail"]["rateList"]:
                comment = Comment()
                comment['attribute'] = {}
                comment['product_id'] = response.meta['product_id']
                comment['comment_id'] = rate['id']
                if "rateDate" in rate.keys():
                    comment['creationTime'] = rate['rateDate']
                else:
                    comment['creationTime'] = ''
                comment['content'] = rate['rateContent'].strip().replace("\n", "")
                comment['item_type'] = 'comment'
                comment['referenceName'] = rate['auctionSku']
                if len(rate['pics']) > 0:
                    comment['attribute']['pics'] = True
                comment['attribute']['appendComment'] = rate['appendComment']
                if "tamllSweetLevel" in rate.keys():
                    comment['attribute']['userlevel'] = rate['tamllSweetLevel']
                if rate['attributesMap'] != '' and rate['attributesMap'].containsKey('worth_score'):
                    comment['attribute']['worth_score'] = rate['attributesMap']['worth_score']
                comment['attribute']['aliMallSeller'] = rate['aliMallSeller']
                comment['attribute']['auctionPrice'] = rate['auctionPrice']
                yield comment
        except Exception, e:
            print str(e)
            # with open("error.txt", "a") as f:
            #     f.write(str(e) + '\n')
            #     f.write(body1 + '\n')
            #     f.write(mstr + '\n\n')
            # lost = Lost()
            # lost['item_type'] = 'lost'
            # lost['url'] = response.url
            # lost['content'] = str(e)
            # lost['page'] = response.meta['page']
            # lost['product_id'] = response.meta['product_id']
            # lost['valid'] = 1
            # yield lost
