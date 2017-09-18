# -*- coding: utf-8 -*-
import pandas as pd
import scrapy
from crawls.items import HotLineItem
import re


class Mcr(scrapy.Spider):
    name = "hotline"

    start_urls = ['http://hotline.ua/musical_instruments/elektrogitary']

    def create_item(self, name, price, img):
        item = HotLineItem()
        item['name'] = name
        item['price'] = price
        item['img'] = img
        return item

    def custom_extractor(self, response, expression):
        data = response.xpath(expression).extract_first()
        return data.strip() if data else ''

    def parse(self, response):
        for item in response.xpath('//div[@data-card_box]'):
            name = self.custom_extractor(item, './div/div/div[2]/div/b/a/text()')
            img = self.custom_extractor(item, './div/div/div/@hltip')
            price = self.custom_extractor(item, './div/div/div[3]/div[2]/div/div[2]/b/text()')
            price = price if price != '' else self.custom_extractor(item, './div/div/div[3]/div[2]/div/div/text()')
            price = price if price != '' else self.custom_extractor(item, './div/div/div[3]/div[2]/div/div/b/text()')
            img = response.urljoin(img) if img != '' else ''
            yield self.create_item(name, price, img)
        nexp_page = response.xpath('//*[@data-id="pager-next"]/@href').extract_first()
        if nexp_page:
        	yield scrapy.Request(url=response.urljoin(nexp_page), callback=self.parse)







