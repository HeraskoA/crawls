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
    file_name = Field()


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

class WegItem(Item):
    ids         = Field()
    catalog_number        = Field()
    descr         = Field()
    add_descr       = Field()
    img_url = Field()

class WegelectricItem(Item):
    ids         = Field()
    catalog_number        = Field()
    add_descr       = Field()
    img_url = Field()

class PatriotItem(Item):
    ids         = Field()
    catalog_number        = Field()
    descr = Field()

class TestGatesItem(Item):
    catalog_number  = Field()

class RegalptsDescrItem(Item):
    ids         = Field()
    brand        = Field()
    catalog_number = Field()
    descr = Field()

class RegalptsDocumentsItem(Item):
    ids         = Field()
    brand        = Field()
    catalog_number = Field()
    name = Field()
    url = Field()

class RegalptsItem(Item):
    ids = Field()
    brand = Field()
    catalog_number = Field()
    cad = Field()

class RegalptsImageItem(Item):
    ids = Field()
    brand = Field()
    catalog_number = Field()
    url = Field()

class McrItem(Item):
    ids = Field()
    catalog_number = Field()
    img_url = Field()
    doc_name = Field()
    doc_url = Field()
    add_descr = Field()

class ToshibaItem(Item):
    ids = Field()
    catalog_number = Field()
    image = Field()
    description = Field()
    specifications = Field()
    ids = Field()

class BaldorDodgeItem(Item):
    ids = Field()
    catalog_number = Field()
    description = Field()
    img = Field()
    specs = Field()
    doc_name = Field()
    doc_url = Field()

class CrownItem(Item):
    ids = Field()
    catalog_number = Field()
    description = Field()
    sku = Field()
    img = Field()
    additional_description = Field()
    name = Field()
    url = Field()

class HotLineItem(Item):
    name = Field()
    price = Field()
    img = Field()

class RexnordItem(Item):
    ids = Field()
    catalog_number = Field()
    name = Field()
    url = Field()