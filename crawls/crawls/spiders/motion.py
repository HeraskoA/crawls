# -*- coding: utf-8 -*-
import pandas as pd
import scrapy


df = pd.read_csv("/data/work/virtualenvs/scrapy/crawls/crawls/spiders/data/Dodge_alternate_2.csv", sep=',')
df['product_substitutions'] = 'none'

class Motion(scrapy.Spider):
    name = "motion"
 
    def start_requests(self):
        i = -1
        for row in df['catalog_number']:
            i = i + 1
            url = 'https://www.motionindustries.com/productCatalogSearch.jsp?q=%s&sw=%s' % (row, row)
            yield scrapy.Request(url=url, callback=self.parse_item, meta={'number_row': i})

    def parse_item(self, response):
        index = int(response.meta['number_row'])
        row = ''
        for item in response.xpath('//*[@id="substitute-items"]/div/div/div'):
            row =  item.xpath('h3/a/text()').extract_first().strip() + "; " + row
        df['product_substitutions'][index] = row if row else 'none'

    def closed(self, reason):
        df.to_csv("/data/work/virtualenvs/Pars/test1/test1/spiders/Dodge_alternate_2.csv", index=False)
