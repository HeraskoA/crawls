# -*- coding: utf-8 -*-

import pandas as pd
import scrapy
from crawls.items import RegalptsItem
import urllib
import urllib2
import shutil
from scrapy.http import FormRequest
import re
import zipfile
import os

out = pd.read_csv("crawls/spiders/data/regalpts_error1.csv", sep=',')
catalog = [str(item).strip() for item in list(out.catalog_number)]
brand = [item.strip() for item in list(out.Brand)]
ids = list(out.id)
catalog_ids = dict(zip(catalog, ids))
catalog_brand = dict(zip(catalog, brand))

f = open('crawls/spiders/data/viewstage.txt', 'r')
viewstage = f.read()
f.close()

root = 'regalpts_download/'

class Regalpts(scrapy.Spider):
    name = "regalpts"

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

    def create_item(self, row, cad):
        item = RegalptsItem()
        item['ids'] = catalog_ids[row]
        item['catalog_number'] = row
        item['brand'] = catalog_brand[row]
        item['cad'] = cad
        return item

    def parse_item(self, response):
        row = response.meta['row']
        if 'Group' in response.url:
            expression = '//a[text()="%s"]/@href' % row
            url = response.xpath(expression).extract_first()
            if url:
                return scrapy.Request(url=url,
                                    callback=self.parse_item,
                                    errback=lambda failure: self.request(row),
                                    dont_filter=True,
                                    meta={'row': row}
                                    )
        elif 'PartID' in response.url:
            url = response.xpath('//*[@title="CAD Drawing"]/@href').extract_first()
            if url:
                return self.download_item(url, row)
            else:
                return self.create_item(row, '')
        else:
            return self.create_item(row, '')

    def download_item(self, url, row):
        formdata={
            '__EVENTTARGET':'Master$ContentPlaceHolder1$ButtonDownload',
            '__EVENTARGUMENT':'',
            '__LASTFOCUS':'',
            '__VIEWSTATE': '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BB8ABRNQYXJhc29saWQgVGV4dC0xMi4xHwZoZGQUKwACDxYEHwAFE1BhcmFzb2xpZCBUZXh0LTEyLjAfBmhkZBQrAAIPFgQfAAUTUGFyYXNvbGlkIFRleHQtMTEuMR8GaGRkFCsAAg8WBB8ABRNQYXJhc29saWQgVGV4dC0xMS4wHwZoZGQUKwACDxYEHwAFE1BhcmFzb2xpZCBUZXh0LTEwLjAfBmhkZBQrAAIPFgQfAAUSUGFyYXNvbGlkIFRleHQtOS4xHwZoZGQUKwACDxYEHwAFElBhcmFzb2xpZCBUZXh0LTkuMB8GaGRkFCsAAg8WBB8ABRJQYXJhc29saWQgVGV4dC04LjAfBmhkZBQrAAIPFgQfAAUWRWRyYXdpbmcgUGFydC9Bc3NlbWJseR8GaGRkDxZSZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZhYBBXdUZWxlcmlrLldlYi5VSS5SYWRDb21ib0JveEl0ZW0sIFRlbGVyaWsuV2ViLlVJLCBWZXJzaW9uPTIwMTUuMS40MDEuMzUsIEN1bHR1cmU9bmV1dHJhbCwgUHVibGljS2V5VG9rZW49MTIxZmFlNzgxNjViYTNkNBaoAWYPDxYEHghDc3NDbGFzcwUJcmNiSGVhZGVyHgRfIVNCAgJkZAIBDw8WBB8HBQlyY2JGb290ZXIfCAICZGQCAg8PFgQfAAUNU2VsZWN0IEZvcm1hdB8GZ2RkAgMPDxYEHwAFHVNPTElEV09SS1MgUGFydC9Bc3NlbWJseS0yMDE3HwZoZGQCBA8PFgQfAAUdU09MSURXT1JLUyBQYXJ0L0Fzc2VtYmx5LTIwMTYfBmhkZAIFDw8WBB8ABR1TT0xJRFdPUktTIFBhcnQvQXNzZW1ibHktMjAxNR8GaGRkAgYPDxYEHwAFJkNBVElBIFY1IFBhcnQvQXNzZW1ibHktVjUtNlIyMDEyIChSMjIpHwZoZGQCBw8PFgQfAAUKQU5WSUwtNTAwMB8GaGRkAggPDxYEHwAFFUFzaGxhci1WZWxsdW0gQXJnb24tNB8GaGRkAgkPDxYEHwAFFkFzaGxhci1WZWxsdW0gQ29iYWx0LTQfBmhkZAIKDw8WBB8A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MR8GaGRkAkwPDxYEHwAFE1BhcmFzb2xpZCBUZXh0LTEyLjAfBmhkZAJNDw8WBB8ABRNQYXJhc29saWQgVGV4dC0xMS4xHwZoZGQCTg8PFgQfAAUTUGFyYXNvbGlkIFRleHQtMTEuMB8GaGRkAk8PDxYEHwAFE1BhcmFzb2xpZCBUZXh0LTEwLjAfBmhkZAJQDw8WBB8ABRJQYXJhc29saWQgVGV4dC05LjEfBmhkZAJRDw8WBB8ABRJQYXJhc29saWQgVGV4dC05LjAfBmhkZAJSDw8WBB8ABRJQYXJhc29saWQgVGV4dC04LjAfBmhkZAJTDw8WBB8ABRZFZHJhd2luZyBQYXJ0L0Fzc2VtYmx5HwZoZGQCEQ9kFgICAQ8WAh4Dc3JjBbMBaHR0cDovL3d3dy4zZHB1Ymxpc2hlci5uZXQvU1dTZXJ2aWNlL291dGZpbGUzZHdlYmdsLmFzcD92aWV3ZmlsZT0vU1dEb3dubG9hZHMxLzIwNDQzNjEyMTMtNDY1ODAxLzJBMkFLNDkwNzI0MjAxNzk1MzkuRVBSVCZiZz0lMjNGRkZGRkYmZmM9JTIzNjY2NjY2Jmg9Mjc1Jnc9Mjc1JmxzPTEmZnM9MSZscD01JmtwPTJkAhMPEGRkFgFmZBgCBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WAQUxTWFzdGVyJENvbnRlbnRQbGFjZUhvbGRlcjEkUmFkQ29tYm9Cb3hGaWxlRm9ybWF0cwUxTWFzdGVyJENvbnRlbnRQbGFjZUhvbGRlcjEkUmFkQ29tYm9Cb3hGaWxlRm9ybWF0cw8UKwACBQ1TZWxlY3QgRm9ybWF0ZWT3JxczJIbIMEWUqIp09Mhw1+/IUw==',
            '__VIEWSTATEGENERATOR':'F0713377',
            '__EVENTVALIDATION':'/wEWBQLUoKqBBgKXvcT9DgKUvcT9DgKa0t6NAgL92JX2CESZU2YXpIAgRWMCcrzIckTOZSRT',
            'Master$ContentPlaceHolder1$RadComboBoxFileFormats':'IGES',
            'Master_ContentPlaceHolder1_RadComboBoxFileFormats_ClientState':'{"logEntries":[],"value":"","text":"IGES","enabled":true,"checkedIndices":[],"checkedItemsTextOverflows":false}',
            'Master$ContentPlaceHolder1$RadioButtonListDimension':'3D'
        }
        req = urllib2.Request('http://edge.regalpts.com/edge/CAD/' + url)
        req.add_data(urllib.urlencode(formdata))
        try:
            resp = urllib2.urlopen(req)
            name = '%s.zip' % row.replace('/', '_')
            print resp.geturl()
            f = open(root + name, 'wb')
            f.write(resp.read())
            f.close()
        except Exception:
            return self.create_item(row, '')
        else:
            with open(root + name, 'r') as file:
                file.seek(0, os.SEEK_END)
                if file.tell() == 0:
                    os.remove(root + name)
                    return self.create_item(row, 'error')
            if zipfile.is_zipfile(root + name):
                return self.create_item(row, name)
            elif 'edge.regalpts.com' in resp.geturl():
                return self.create_item(row, '')
            else:
                return self.request(row)
