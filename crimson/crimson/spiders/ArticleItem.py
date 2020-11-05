import scrapy
from scrapy.loader.processors import MapCompose
from w3lib.html import remove_tags


class ArticleItem(scrapy.Item):
    title = scrapy.Field(input_processor=MapCompose(remove_tags))
    author = scrapy.Field(input_processor=MapCompose(remove_tags))
    body = scrapy.Field(input_processor=MapCompose(remove_tags))
