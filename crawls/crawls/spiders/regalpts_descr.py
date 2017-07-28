# -*- coding: utf-8 -*-

import pandas as pd
import scrapy
from crawls.items import RegalptsDescrItem
import urllib
import urllib2
import shutil
from scrapy.http import FormRequest
import re
import zipfile
import os

out = pd.read_csv("/data/work/virtualenvs/scrapy/crawls/crawls/spiders/data/Regal_Beloit_aux_descriptions.csv", sep=',')
catalog = list(out.catalog_number)
brand = list(out.Brand)
ids = list(out.id)
catalog_ids = dict(zip(catalog, ids))
catalog_brand = dict(zip(catalog, brand))
f = open('crawls/spiders/data/viewstage.txt', 'r')
viewstage = f.read()
f.close()


class Regalpts(scrapy.Spider):
    name = "regalpts_descr"

    def start_requests(self):
        for row in out['catalog_number']:
            yield self.request(row)

    def request(self, meta_row):
        row = str(meta_row).strip()
        url = 'http://edge.regalpts.com/EDGE/CAD/Default.aspx?SS=yes'
        formdata = {
        '__EVENTTARGET':'',
        '__EVENTARGUMENT':'',
        '__VIEWSTATE': viewstage,
        '__VIEWSTATEGENERATOR':'CC83E274',
        '__EVENTVALIDATION':'/wEWBgK0w53LDQLjqMbGAQKW/Y24DgLJ/9mgDgKnipiBAQLyy5/lAnAMSE4GnkVeEYUcKuBELFKIEU1Z',
        'ctl00_Master_ContentPlaceHolder1_MenuPanel_ClientState':'{"expandedItems":["0"],"logEntries":[],"selectedItems":[]}',
        'ctl00$Master$ContentPlaceHolder1$ContentPlaceHolderMain$TextBoxPartNumber': row,
        'ctl00$Master$ContentPlaceHolder1$ContentPlaceHolderMain$ButtonPartSearch':'SEARCH >',
        'ctl00_Master_ContentPlaceHolder1_ContentPlaceHolderMain_RadTreeViewProductLine_ClientState':'{"expandedNodes":[],"collapsedNodes":[],"logEntries":[],"selectedNodes":[],"checkedNodes":[],"scrollPosition":0}',
        'ctl00_Master_ContentPlaceHolder1_ContentPlaceHolderMain_RadWindowOpenPDF_ClientState':'',
        'ctl00_Master_ContentPlaceHolder1_ContentPlaceHolderMain_RadWindowManagerOpenPDF_ClientState':'',
        'ctl00_Master_ContentPlaceHolder1_RadWindowNemaStandards_ClientState':'',
        'ctl00_Master_ContentPlaceHolder1_RadWindowIECStandards_ClientState':'',
        'ctl00_Master_ContentPlaceHolder1_RadWindowManagerPopups_ClientState':''
        }
        return FormRequest(url=url, 
                            callback=self.parse_item,
                            errback=lambda failure: self.request(meta_row),
                            dont_filter=True,
                            formdata=formdata,
                            meta={'meta_row': meta_row}
                            )

    def create_item(self, meta_row, table):
        item = RegalptsDescrItem()
        item['ids'] = catalog_ids[meta_row]
        item['brand'] = catalog_brand[meta_row].strip()
        item['catalog_number'] = str(meta_row).strip()
        item['descr'] = table
        return item

    def parse_item(self, response):
        meta_row = response.meta['meta_row']
        print response.url
        if 'Group' in response.url:
            expression = '//a[text()="%s"]/@href' % str(meta_row).strip()
            url = response.xpath(expression).extract_first()
            if url:
                return scrapy.Request(url=url,
                                    callback=self.extract_table,
                                    errback=lambda failure: self.request(meta_row),
                                    dont_filter=True,
                                    meta={'meta_row': meta_row}
                                    )
        elif 'PartID' in response.url:
            return self.extract_table(response)
        else:
            return self.create_item(meta_row, '')

    def extract_table(self, response):
        meta_row = response.meta['meta_row']
        table = response.xpath('//*[@id="ctl00_Master_ContentPlaceHolder1_ContentPlaceHolderMain_RadGridPartDetailInfo_ctl00"]').extract_first()
        return self.create_item(meta_row, table)


