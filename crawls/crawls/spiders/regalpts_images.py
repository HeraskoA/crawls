# -*- coding: utf-8 -*-

import pandas as pd
import scrapy
from crawls.items import RegalptsImageItem
import urllib
import urllib2
import shutil
from scrapy.http import FormRequest
import re
import zipfile
import os

out = pd.read_csv("crawls/spiders/data/Regal_Beloit_images.csv", sep=',')
catalog = [str(item).strip() for item in list(out.catalog_number)]
brand = [item.strip() for item in list(out.Brand)]
ids = list(out.id)
catalog_ids = dict(zip(catalog, ids))
catalog_brand = dict(zip(catalog, brand))
f = open('crawls/spiders/data/viewstage.txt', 'r')
viewstage = f.read()
f.close()


class Regalpts(scrapy.Spider):
    name = "regalpts_img"

    def start_requests(self):
        for row in catalog:
            yield self.request(row)

    def request(self, row):
        url = 'http://edge.regalpts.com/EDGE/CAD/Default.aspx?SS=yes'
        formdata = {
        '__EVENTTARGET':'',
        '__EVENTARGUMENT':'',
        '__VIEWSTATE': viewstage,
        '__VIEWSTATEGENERATOR':'CC83E274',
        '__EVENTVALIDATION':'/wEWBgL4+JvjBALjqMbGAQKW/Y24DgLJ/9mgDgKnipiBAQLyy5/lAuF2uu8b/BgziUqSvX9FGHOhGpdW',
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
                            errback=lambda failure: self.request(row),
                            dont_filter=True,
                            formdata=formdata,
                            meta={'row': row}
                            )

    def create_item(self, row, url):
        item = RegalptsImageItem()
        item['ids'] = catalog_ids[row]
        item['brand'] = catalog_brand[row]
        item['catalog_number'] = row
        item['url'] = url
        return item

    def parse_item(self, response):
        row = response.meta['row']
        if 'Group' in response.url:
            expression = '//a[text()="%s"]/@href' % row
            url = response.xpath(expression).extract_first()
            if url:
                return scrapy.Request(url=url,
                                    callback=self.extract_img,
                                    errback=lambda failure: self.request(row),
                                    dont_filter=True,
                                    meta={'row': row}
                                    )
        elif 'PartID' in response.url:
            return self.extract_img(response)
        else:
            return self.create_item(row, '')

    def extract_img(self, response):
        row = response.meta['row']
        img = response.xpath('//*[@id="ctl00_Master_ContentPlaceHolder1_ContentPlaceHolderMain_ImagePartDetailTabPartPhoto"]/@src').extract_first()
        return self.create_item(row, response.urljoin(img)) if img else self.create_item(row, '')

