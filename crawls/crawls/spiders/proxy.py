# -*- coding: utf-8 -*-
import pandas as pd
import scrapy
from crawls.items import ProxyItem
import random, re
 
class Dixon(scrapy.Spider):
    name = "proxy"
    start_urls = [
        'https://free-proxy-list.net/',
    ]

    def parse(self, response):
        for row in response.xpath('//*[@id="proxylisttable"]/tbody/tr'):
            proxy = row.xpath('td[1]/text()').extract_first() + ':' + row.xpath('td[2]/text()').extract_first()
            item = ProxyItem()
            item['proxy'] = proxy
            yield item




