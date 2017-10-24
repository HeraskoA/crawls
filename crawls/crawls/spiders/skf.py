# -*- coding: utf-8 -*-

import pandas as pd
import scrapy
from crawls.items import SkfItem
import urllib
from scrapy.http import FormRequest
import re

out = pd.read_csv("crawls/spiders/data/skf_bearings.csv", sep=',')
out['cad'] = ''
catalog = list(out.catalog_number)
ids = list(out.id)
catalog_ids = dict(zip(catalog, ids))


class Dixon(scrapy.Spider):
    name = "skf"

    def start_requests(self):
        for row in out['catalog_number']:
            meta_row = row
            row = urllib.quote_plus(row.strip())
            url = 'http://webassistants.partcommunity.com/23d-libs/skf/mapping/get_mident_index_designation.vbb?designation=' + row
            yield scrapy.Request(url=url, callback=self.parse_item, errback=self.error, meta={'row': meta_row })

    def error(self, row):
        item = SkfItem()
        item['ids'] = catalog_ids[row]
        item['catalog_number'] = row.strip()
        item['cad'] = 'none'
        return item


    def parse_item(self, response):
        if 'error' in response.xpath('//*').extract_first():
            return self.error(response.meta['row'])
    	prj_path = response.xpath('//*').re(r'{"prjPath":"(.+)","fixName')[0]
    	productid = response.xpath('//*').re(r'"fixValue":"(.+)"')[0]
    	part = '{' + prj_path + '},{PRODUCTID=' + productid + '}'
    	form_data = {}
    	form_data['cgiaction'] = 'download'
    	form_data['downloadflags'] = 'ZIP'
    	form_data['firm'] = 'skf'
    	form_data['language'] = 'english'
    	form_data['server_type'] = 'SUPPLIER_EXTERNAL_skf'
    	form_data['format'] = 'DXF3D-AUTOCAD VERSION 2013'
    	form_data['part'] = part
    	return FormRequest(url="http://www.skf.com/ajax/cadDownload.json",
                    formdata=form_data, callback=self.parse_item1, meta={'row': response.meta['row']})

    def parse_item1(self, response):
    	url = response.xpath('//*').re(r'{"downloadURL":"(.+)"')[0]
    	return scrapy.Request(url=url, errback=self.repeat, callback=self.parse_item2, meta={'row': response.meta['row'], 'url': url})

    def repeat(self, failure):
        response = failure.value.response
        url = response.meta['url']
        return scrapy.Request(url=url, errback=self.repeat, callback=self.parse_item2, meta={'row': response.meta['row'], 'url': url})


    def parse_item2(self, response):
        orderno = response.xpath('//*').re(r'<ORDERNO>(.+)</ORDERNO>')[0] + '/'
        zipfile = response.xpath('//*').re(r'<ZIPFILE>(.+)</ZIPFILE>')[0]
        item = SkfItem()
        item['ids'] = catalog_ids[response.meta['row']]
        item['catalog_number'] = response.meta['row'].strip()
        item['cad'] = 'http://www.skf.com/cadDownload/' + orderno + zipfile
        return item








