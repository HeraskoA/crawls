# -*- coding: utf-8 -*-
import pandas as pd
import scrapy
from crawls.items import GatesItem
import random, re
import json
from urllib import urlopen
import urllib
import urllib2
import shutil
 

out = pd.read_csv("crawls/spiders/data/gates_full.csv", sep=',')
catalog = list(out.catalog_number)
ids = list(out.id)
catalog_ids = dict(zip(catalog, ids))

proxy = pd.read_csv("crawls/spiders/data/proxy.csv", sep=',')
proxy_list = list(proxy.proxy)

class Dixon(scrapy.Spider):
    name = "gates1"
    index = 0

    def get_proxy(self, change=0):
        self.index = self.index + 1 if change else self.index
        try:
            proxy = proxy_list[self.index]
        except Exception:
            raise scrapy.exceptions.CloseSpider('empty poxy list')
        else:
            return proxy

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
        return scrapy.Request(url=url, callback=callback, errback=errback, meta={ 'download_timeout': 20}, dont_filter=True)

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
                req = urllib2.Request('http:' + url)
                resp = urllib2.urlopen(req)
                file_name = '%s.zip' % urllib.quote_plus(str(meta_row).strip())
                with open('gates_downoad/' + file_name, 'wb') as file:
                    shutil.copyfileobj(resp.fp, file)
            except Exception:
                item['cad'] = ''
            else:
                item['cad'] = file_name
            print self.index
            return item



