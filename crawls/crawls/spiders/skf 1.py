# -*- coding: utf-8 -*-

import pandas as pd
import scrapy
from crawls.items import SkfItem
import urllib
import urllib2
from scrapy.http import FormRequest
import re

out = pd.read_csv("/data/work/virtualenvs/scrapy/crawls/crawls/spiders/data/skf_bearings.csv", sep=',')
out['cad'] = ''
catalog = list(out.catalog_number)
ids = list(out.id)
catalog_ids = dict(zip(catalog, ids))


class Dixon(scrapy.Spider):
    name = "skf1"

    def start_requests(self):
        for row in out['catalog_number']:
            meta_row = row
            row = urllib.quote_plus(str(row).strip())
            url = 'http://www.skf.com/group/system/SearchResult.html?search=' + row
            yield scrapy.Request(url=url, callback=self.parse_item1, errback=self.repeat29, meta={'row': meta_row })

    def repeat29(self, failure):
        row = failure.value.response.meta['row']
        meta_row = row
        row = urllib.quote_plus(str(row).strip())
        url = 'http://www.skf.com/group/system/SearchResult.html?search=' + row
        return scrapy.Request(url=url, callback=self.parse_item1, errback=self.repeat29, meta={'row': meta_row })

    def error(self, row):
        item = SkfItem()
        item['ids'] = catalog_ids[row]
        item['catalog_number'] = str(row).strip()
        item['file_urls'] = ''
        return item

    def parse_item1(self, response):
        if response.xpath('//*[@id="skf-search-form"]/div[2]/div[2]/ul/li[1]/div/div[1]/ul/li[2]/a/span/text()').extract_first() == str(response.meta['row']).strip():
            url = response.xpath('//*[@id="skf-search-form"]/div[2]/div[2]/ul/li[1]/div/div[1]/ul/li[2]/a/@href').re(r'prodid=(.+)&pubid')[0]
            url = urllib2.unquote(url)
            url = urllib.quote_plus(url)
            url = 'http://webassistants.partcommunity.com/23d-libs/skf/mapping/get_mident_index_designation.vbb?designation=' + url
            return scrapy.Request(url=url, callback=self.parse_item, errback=self.error, meta={'row': response.meta['row']})
        else:
            return self.error(response.meta['row'])


    def parse_item(self, response):
        if 'error' in response.xpath('//*').extract_first():
            return self.error(response.meta['row'])
    	prj_path = response.xpath('//*').re(r'{"prjPath":"(.+)","fixName')[0]
    	productid = response.xpath('//*').re(r'"fixValue":"(.+)"')[0]
        fix_name = response.xpath('//*').re(r'"fixName":"(.+)"')[0]
    	part = '{' + prj_path + '},{' + fix_name + '=' + productid + '}'
    	form_data = {}
    	form_data['cgiaction'] = 'download'
    	form_data['downloadflags'] = 'ZIP'
    	form_data['firm'] = 'skf'
    	form_data['language'] = 'english'
    	form_data['server_type'] = 'SUPPLIER_EXTERNAL_skf'
    	form_data['format'] = 'DXF3D-AUTOCAD VERSION 2013'
    	form_data['part'] = part
    	return FormRequest(url="http://www.skf.com/ajax/cadDownload.json",
                    formdata=form_data, errback=self.repeat29, callback=self.parse_item3, meta={'row': response.meta['row']})

    def parse_item3(self, response):
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
        item['catalog_number'] = str(response.meta['row']).strip()
        item['file_urls'] = ['http://www.skf.com/cadDownload/' + orderno + zipfile]
        return item








