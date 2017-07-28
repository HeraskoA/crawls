# -*- coding: utf-8 -*-
import pandas as pd
import scrapy
from crawls.items import TestGatesItem
import random, re
import json
from urllib import urlopen
import urllib
import urllib2
import shutil
 

out = pd.read_csv("/data/work/virtualenvs/scrapy/crawls/gates_rubber_result.csv", sep=',')
cad = list(out.cad)
catalog = list(out.catalog_number)
catalog_cad = dict(zip(cad, catalog))


class Gates(scrapy.Spider):
    name = "test_gates"

    def start_requests(self):
        for url in cad:
            if str(url) != 'nan':
                errback = lambda failure: self.invalid(url)
                yield scrapy.Request(url=url, callback=self.valid, errback=errback, dont_filter=True)

    def valid(self, response):
        pass

    def invalid(self, url):
        item = TestGatesItem()
        item['catalog_number'] = catalog_cad[url]
        return item





