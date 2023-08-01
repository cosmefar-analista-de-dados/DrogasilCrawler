import scrapy

class DrogasilItem(scrapy.Item):

    url = scrapy.Field()
    sku = scrapy.Field()
    EAN = scrapy.Field()
    product = scrapy.Field()
    brand = scrapy.Field()
    quantity = scrapy.Field()
    weight = scrapy.Field()
    manufacturer = scrapy.Field()
    description = scrapy.Field()
    category = scrapy.Field()
    sub_category = scrapy.Field()
    price = scrapy.Field()