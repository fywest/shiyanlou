# -*- coding: utf-8 -*-
# import scrapy
#
#
# class AwesomeMovieSpider(scrapy.Spider):
#     name = 'awesome_movie'
#     allowed_domains = ['movie.douban.com']
#     start_urls = ['http://movie.douban.com/']
#
#     def parse(self, response):
#         pass
# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
# from douban_movie.items import MovieItem
from ..items import MovieItem

class AwesomeMovieSpider(scrapy.spiders.CrawlSpider):

    name = 'awesome-movie'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/subject/3011091/']

    rules = (
        # Rule("TODO: 实现爬取策略"),
        Rule(LinkExtractor(allow=r'https://movie.douban.com/subject/.+/?from=subject-page'), callback='parse_page',
             follow=True),
    )


    def parse_movie_item(self, response):
        "TODO: 解析 item"
        item = MovieItem()
        item['url'] = response.url
        item['name'] = response.xpath('//span[@property="v:itemreviewed"]/text()').extract_first()
        item['summary'] = response.xpath('//span[@property="v:summary"]/text()').extract_first()
        item['score'] = response.xpath('//strong[@property="v:average"]/text()').extract_first()
        return item

    def parse_start_url(self, response):
        yield self.parse_movie_item(response)


    def parse_page(self, response):
        yield self.parse_movie_item(response)