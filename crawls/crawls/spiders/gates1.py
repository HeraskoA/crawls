# -*- coding: utf-8 -*-
import pandas as pd
import scrapy
from crawls.items import GatesItem
import random, re
import json
from urllib import urlopen
 

out = pd.read_csv("/data/work/virtualenvs/scrapy/crawls/crawls/spiders/data/gates.csv", sep=',')
catalog = list(out.catalog_number)
ids = list(out.id)
catalog_ids = dict(zip(catalog, ids))

proxy = pd.read_csv("/data/work/virtualenvs/scrapy/crawls/crawls/spiders/data/proxy.csv", sep=',')
proxy_list = list(proxy.proxy)

class Dixon(scrapy.Spider):
    name = "gates1"
    index = 0
    '''
    def get_random_proxy(self):
        url = urlopen('https://gimmeproxy.com/api/getProxy?get=true').read()
        url = json.loads(url)
        return re.findall(r'//(.+)', url['curl'])[0]
    '''
    def get_proxy(self, change=0):
        self.index = self.index + 1 if change else self.index
        return proxy_list[self.index]

    def start_requests(self):
        for row in out['catalog_number']:
            meta_row = row
            row = self.replace_symbols(str(row).strip())
            url = 'http://partview.gates.com/catalog3/cad?d=gates.pt&id=' + row + '&f=dxf'
            proxy = self.get_proxy()
            yield self.request(url, meta_row, row, proxy)

    def request(self, url, meta_row, row, proxy):
        callback = lambda response: self.parse_item(response, meta_row, row, url)
        errback = lambda failure: self.repeat(failure, url, meta_row, row)
        return scrapy.Request(url=url, callback=callback, errback=errback, meta={'proxy': proxy})

    def repeat(self, failure, url, meta_row, row):
        proxy = self.get_proxy(1)
        return self.request(url, meta_row, row, proxy)

    def replace_symbols(self, row):
        return row.replace('/', '_').replace('.', '-')

    def parse_item(self, response, meta_row, row, url):
        if 'restricted access' in response.xpath('//*').extract_first():
            proxy = self.get_proxy(1)
            return self.request(url, meta_row, row, proxy)
        else:
            item = GatesItem()
            item['ids'] = catalog_ids[meta_row]
            item['catalog_number'] = str(meta_row).strip()
            try:
                url = response.xpath('//*').re(r'"url":"(.+)","productID"')[0]
            except Exception:
                item['cad'] = 'none'
            else:
                item['cad'] = 'http:' + url
            print self.index
            return item



