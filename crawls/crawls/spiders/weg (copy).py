# -*- coding: utf-8 -*-
import pandas as pd
import scrapy
import urllib
import urllib2
from crawls.items import EItem
from scrapy.http import FormRequest
import re

out = pd.read_csv("crawls/spiders/data/0695487001508855201_0.csv", sep=',')
catalog_item_codes = [str(item).strip() for item in out.item_code]
ids = list(out.id)
#description = list(out.description)
ordering_number = list(out.ordering_number)
item_codes_ids = dict(zip(catalog_item_codes, ids))
#item_codes_description = dict(zip(catalog_item_codes, description))


class Weg(scrapy.Spider):
    name = "e-services"

    start_urls = ['https://www.e-services.flexco.com/eCollaboration/ecatalog/aspx/ParameterListing.aspx?Source=&IndustryID=0&ProductID=2763&ParameterID=Size&Value=R2&Mode=Value&View=']

    def parse(self, response):
        item_codes = response.xpath('//tr[@class="paramvalues"]/td[3]/text()').extract()
        for code in item_codes:
            if code in catalog_item_codes:
                url = response.xpath('//td[@class="formnames" and text()="%s"]/../td[6]/a/@href' % code).extract_first()
                yield scrapy.Request(url=response.urljoin(url), callback=self.parse_item2)
        if 

    def parse_item2(self, response):
        print response.xpath('//*[@id="ctl00_ContentPlaceHolder1_dlSpecs"]').extract_first()
        #table = response.xpath('//table/').extract_first()



