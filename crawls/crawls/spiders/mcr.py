# -*- coding: utf-8 -*-
import pandas as pd
import scrapy
from crawls.items import McrItem
import re


out = pd.read_csv("crawls/spiders/data/MCR_2.csv", sep=',')
catalog = [str(item).strip() for item in list(out.catalog_number)]
ids = list(out.id)
catalog_ids = dict(zip(catalog, ids))


class Mcr(scrapy.Spider):
    name = "mcr"

    def start_requests(self):
        for row in catalog:
            yield self.request(row)

    def request(self, row):
        url = 'http://www.mcrsafety.com/search?s=' + row
        return scrapy.Request(url=url, 
                            callback=self.parse_item,
                            errback=lambda failure: self.request(row),
                            dont_filter=True,
                            meta={'row': row}
                            )

    def create_item(self, row, img_url, doc_name, doc_url, add_descr):
        item = McrItem()
        item['ids'] = catalog_ids[row]
        item['catalog_number'] = row
        item['img_url'] = img_url
        item['doc_name'] = doc_name
        item['doc_url'] = doc_url
        item['add_descr'] = add_descr
        return item

    def custom_extractor(self, response, expression):
        data = response.xpath(expression).extract_first()
        return data if data else ''

    def construct_table(self, table):
        table = re.sub(r'<div class="row">(\n|\s)+<div class="col-md-6 col-sm-12">(\n|\s)+<dl class="dl-horizontal">', '<table>', table)
        table = re.sub(r'</dl>(\n|\s)+</div>(\n|\s)+<div class="col-md-6 col-sm-12(\n|\s)+left-column">(\n|\s)+<dl class="dl-horizontal">', '', table)
        table = re.sub(r'</dl>(\n|\s)+</div>(\n|\s)+</div>(\n|\s)+<!-- SPC Attributes -->(\n|\s)+</div>', '</table>', table)
        table = re.sub(r'</dt>(\n|\s)+<dd>', '</td><td>', table)
        table = table.replace('<dt>', '<tr><td>')
        table = table.replace('</dd>', '</td></tr>')
        return table

    def parse_item(self, response):
        row = response.meta['row']
        expression = '//h3[text()="%s"]/../@href' % row
        url = response.xpath(expression).extract_first()
        return scrapy.Request(url=response.urljoin(url),
                                callback=self.extract_data,
                                errback=lambda failure: self.request(row),
                                dont_filter=True,
                                meta={'row': row}
                                ) if url else self.create_item(row, '', '', '', '')

    def extract_data(self, response):
        row = response.meta['row']
        descr = self.custom_extractor(response, '//*[@id="page_content"]/div[2]/div/div[2]/div[2]/div[1]/div[2]/div[2]')
        sizes = self.custom_extractor(response, '//*[@id="page_content"]/div[2]/div/div[2]/div[2]/div[1]/div[2]/div[4]')
        img_url = self.custom_extractor(response, '//*[@id="material_main_image"]/@src')
        doc_url = self.custom_extractor(response, '//*[@id="page_content"]/div[2]/div/div[2]/div[2]/div[1]/div[2]/div[5]/a/span/../@href')
        doc_url = response.urljoin(doc_url) if doc_url != '' else ''
        doc_name = self.custom_extractor(response, '//*[@id="page_content"]/div[2]/div/div[2]/div[2]/div[1]/div[2]/div[5]/a/span/text()')
        features = self.custom_extractor(response, '//*[@id="features"]')
        specs = self.custom_extractor(response, '//*[@id="specs"]')
        specs = self.construct_table(specs) if specs != '' else ''
        industries = self.custom_extractor(response, '//*[@id="industries"]')
        add_descr = descr + sizes + features + specs + industries
        return self.create_item(row, img_url, doc_name, doc_url, add_descr)




