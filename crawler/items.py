import scrapy


class Item(scrapy.Item):
    site = scrapy.Field()
    source_id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    image = scrapy.Field()
