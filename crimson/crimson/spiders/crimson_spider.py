import scrapy

import string
import scrapy
from scrapy import Request

class MySpider(scrapy.Spider):
    name = "crimson"
    start_urls = [
        "https://www.thecrimson.com/sitemap/1952",
    ]

    #response.xpath('//html/body/div[4]/div//a/@href').getall()

    '''def parse(self, response):
        urls = response.xpath('//html/body/div[4]/div//a/@href').getall()
        # formatting
        urls = list(filter(lambda x: x[0] == '/', urls))
        urls = list(map(lambda x: "https://www.thecrimson.com" + x, urls))

        return (Request(url, callback=self.parse_year_page) for url in urls)'''

    def parse(self, response):
        # response.xpath('//html/body/div[4]/div//a/@href').getall()
        urls = response.xpath('//html/body/div[4]/div//a/@href').extract()
        urls = urls[:-60]
        # formatting
        urls = list(filter(lambda x: x[0] == '/', urls))
        urls = list(map(lambda x: "https://www.thecrimson.com" + x, urls))

        return (Request(url, callback=self.parse_day_page) for url in urls)

    def parse_day_page(self, response):
        link = '//html/body/div[4]/div//a/@href'
        urls = response.xpath(link).extract()

        #formatting
        urls = list(filter(lambda x: x[0] == '/', urls))
        urls = list(map(lambda x: "https://www.thecrimson.com" + x, urls))

        return (Request(url, callback=self.parse_article) for url in urls)

    def parse_article(self, response):
        body = response.css('div.css-1hc0jhf p').getall()
        body_str = ' '.join(map(str, body))

        filters = ['Eisenhower', 'Stevenson']

        res = [ele for ele in filters if (ele in body_str)]

        if bool(res):
            yield {
                "title": response.css('title::text').get(),
                "author": response.xpath('/html/body/div[1]/div[5]/div[2]/div[2]/span/a/text()').get(),
                "body": body_str,
             }