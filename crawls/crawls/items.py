# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class Notebook(Item):
	model = Field();

class DixonItem(Item):
    ids         = Field()
    name        = Field()
    url         = Field()

class BaldorItem(Item):
    ids         = Field()
    catalog_number        = Field()
    additional_descr         = Field()

class SkfItem(Item):
    ids         = Field()
    catalog_number        = Field()
    cad         = Field()

class GatesItem(Item):
    ids         = Field()
    catalog_number        = Field()
    cad         = Field()

class ProxyItem(Item):
	proxy = Field()

class Baldor1Item(Item):
    ids         = Field()
    catalog_number        = Field()
    specs_or_overview         = Field()
    description         = Field()

class Baldor2Item(Item):
    ids         = Field()
    catalog_number        = Field()
    name         = Field()
    url         = Field()