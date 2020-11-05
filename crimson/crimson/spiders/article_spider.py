from io import StringIO
from functools import partial

import scrapy
from scrapy.http import Request
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.item import Item
from w3lib.html import remove_tags


class ArticleItem(scrapy.Item):
    title = scrapy.Field(input_processor=MapCompose(remove_tags))
    author = scrapy.Field(input_processor=MapCompose(remove_tags))
    body = scrapy.Field(input_processor=MapCompose(remove_tags))

def find_all_substrings(string, sub):
    import re
    starts = [match.start() for match in re.finditer(re.escape(sub), string)]
    return starts

class WebsiteSpider(CrawlSpider):

    name = "webcrawler"
    start_urls = ["https://www.thecrimson.com/column/the-in-between/article/2020/10/15/heng-presidential-candidates-student-debaters/"]

    def parse(self, response):
        body = response.css('div.css-1hc0jhf p').getall()
        body_str = ' '.join(map(str, body))

        filters = ['trump', 'biden']

        res = [ele for ele in filters if (ele in body_str)]

        '''if str(bool(res)):
        yield {
            "title": response.css('title::text').get(),
            "author": response.xpath('/html/body/div[1]/div[5]/div[2]/div[2]/span/a/text()').get(),
            "body": body_str
        }'''

        l = ItemLoader(item=ArticleItem(), response=response)
        l.add_css('title', 'title::text')
        l.add_xpath('author', '/html/body/div[1]/div[5]/div[2]/div[2]/span/a/text()')
        l.add_css('body', 'div.css-1hc0jhf p')
        return l.load_item()