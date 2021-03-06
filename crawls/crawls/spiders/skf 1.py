# -*- coding: utf-8 -*-

import pandas as pd
import scrapy
from crawls.items import SkfItem
import urllib
import urllib2
from scrapy.http import FormRequest
import re

out = pd.read_csv("crawls/spiders/data/skf_bearings.csv", sep=',')
out['cad'] = ''
catalog = list(out.catalog_number)
ids = list(out.id)
catalog_ids = dict(zip(catalog, ids))


class Dixon(scrapy.Spider):
    name = "skf1"

    def start_requests(self):
        for row in out['catalog_number']:
            yield self.request(row)

    def request(self, meta_row):
        row = urllib.quote_plus(str(meta_row).strip())
        url = 'http://www.skf.com/group/system/SearchResult.html?search=' + row
        callback = lambda response: self.parse_item1(response, meta_row)
        errback = lambda failure: self.repeat(failure, meta_row)
        return scrapy.Request(url=url, callback=callback, errback=errback, dont_filter=True)

    def repeat(self, failure, meta_row):
        return self.request(meta_row)

    def error(self, row):
        item = SkfItem()
        item['ids'] = catalog_ids[row]
        item['catalog_number'] = str(row).strip()
        item['file_urls'] = ''
        return item

    def parse_item1(self, response, meta_row):
        if 'Our apologies, something has gone wrong' in response.xpath('//*').extract_first():
            return self.request(meta_row)
        elif response.xpath('//*[@id="skf-search-form"]/div[2]/div[2]/ul/li[1]/div/div[1]/ul/li[2]/a/span/text()').extract_first() == str(meta_row).strip():
            url = response.xpath('//*[@id="skf-search-form"]/div[2]/div[2]/ul/li[1]/div/div[1]/ul/li[2]/a/@href').re(r'prodid=(.+)&pubid')[0]
            url = urllib2.unquote(url)
            url = urllib.quote_plus(url)
            url = 'http://webassistants.partcommunity.com/23d-libs/skf/mapping/get_mident_index_designation.vbb?designation=' + url
            callback = lambda response: self.parse_item2(response, meta_row)
            errback = lambda failure: self.repeat(failure, meta_row)
            return scrapy.Request(url=url, callback=callback, errback=errback)
        else:
            return self.error(meta_row)


    def parse_item2(self, response, meta_row):
        if 'error' in response.xpath('//*').extract_first():
            return self.error(meta_row)
    	prj_path = response.xpath('//*').re(r'{"prjPath":"(.+)","fixName')[0]
    	productid = response.xpath('//*').re(r'"fixValue":"(.+)"')[0]
        fix_name = response.xpath('//*').re(r'"fixName":"(.+)","fixValue"')[0]
    	part = '{' + prj_path + '},{' + fix_name + '=' + productid + '}'
    	form_data = {}
    	form_data['cgiaction'] = 'download'
    	form_data['downloadflags'] = 'ZIP'
    	form_data['firm'] = 'skf'
    	form_data['language'] = 'english'
    	form_data['server_type'] = 'SUPPLIER_EXTERNAL_skf'
    	form_data['format'] = 'DXF3D-AUTOCAD VERSION 2013'
    	form_data['part'] = part
        callback = lambda response: self.parse_item3(response, meta_row)
        errback = lambda failure: self.repeat(failure, meta_row)
    	return FormRequest(url="http://www.skf.com/ajax/cadDownload.json",
                    formdata=form_data, errback=errback, callback=callback)

    def parse_item3(self, response, meta_row):
    	url = response.xpath('//*').re(r'{"downloadURL":"(.+)"')[0]
        callback = lambda response: self.parse_item4(response, meta_row)
        errback = lambda failure: self.repeat(failure, meta_row)
    	return scrapy.Request(url=url, errback=errback, callback=callback)


    def parse_item4(self, response, meta_row):
        orderno = response.xpath('//*').re(r'<ORDERNO>(.+)</ORDERNO>')[0] + '/'
        zipfile = response.xpath('//*').re(r'<ZIPFILE>(.+)</ZIPFILE>')[0]
        item = SkfItem()
        item['ids'] = catalog_ids[meta_row]
        item['catalog_number'] = str(meta_row).strip()
        item['file_urls'] = ['http://www.skf.com/cadDownload/' + orderno + zipfile]
        return item
