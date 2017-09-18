from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader.processors import Join, MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import TakeFirst
from scrapy.loader import ItemLoader, XPathItemLoader
from scrapy.selector import HtmlXPathSelector, Selector
from scrapy.item import Item, Field
import time
import re

countries = {
    '/us/': 'United States',
    '/fr/': 'France',
}

class AmaniItem(Item):
    name = Field()
    price = Field()
    currency = Field()
    category = Field()
    sku = Field()
    time = Field()
    color = Field()
    size = Field()
    region = Field()
    description = Field()

class ArmaniLoader(XPathItemLoader):
    default_output_processor = TakeFirst()
    size_in = Join('/')
    color_in = Join('/')
    currency_in = MapCompose(lambda s: 'EUR' if 'EUR' == s else 'USD')
    region_in = MapCompose(lambda s: countries[s])


class TestSpider(CrawlSpider):
    name = "armani"
    allowed_domains = ["armani.com"]
    start_urls = ["http://www.armani.com" + country for country in countries]

    rules = (
        Rule(LinkExtractor(allow=('\.html')), callback='parse_item'),
        Rule(LinkExtractor(allow=('subhome', 'salesline')), follow=True),
    )

    def parse_item(self, response):
        loader = ArmaniLoader(AmaniItem(), response)
        start = time.time()
        loader.add_xpath('name', '//*[@id="pageContent"]/article/aside/h1/text()')
        loader.add_xpath('price', '//*[@id="pageContent"]/article/aside/div[3]/div[1]/span[2]/text()')
        loader.add_xpath('currency', '//*[@id="pageContent"]/article/aside/div[3]/div[1]/span[1]/text()')
        referer = response.request.headers.get('Referer')
        category = re.findall(r'/[a-z]{2}/(.+)\?', referer)[0]
        loader.add_value('category', category)
        loader.add_xpath('sku', '//*[@id="pageContent"]/article/aside/h3/span[2]/text()')
        loader.add_xpath('size', '//*[@class="SizeW"]/li/a/text()')
        loader.add_xpath('color', '//*[@class="Colors"]/li/a/text()')
        region = re.findall(r'(/[a-z]{2}/)', response.url)[0]
        loader.add_value('region', region)
        loader.add_xpath('description', '//*[@id="pageContent"]/article/aside/ul[2]/li[1]/div[2]/text()')
        end = time.time()
        loader.add_value('time', end - start)
        return loader.load_item()