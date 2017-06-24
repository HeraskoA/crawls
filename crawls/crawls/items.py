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