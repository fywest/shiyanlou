# -*- coding: utf-8 -*-
import scrapy
from ..items import RepositoryItem

class RepositoriesSpider(scrapy.Spider):
    name = 'repositories'
    start_urls = ['']

    @property
    def start_urls(self):
        url_tmpl = 'https://github.com/shiyanlou?page={}&tab=repositories'
        return (url_tmpl.format(i) for i in range(1, 5))

    def parse(self, response):
        for course in response.xpath('//*[@id="user-repositories-list"]/ul/li'):
            item = RepositoryItem()
            item['name'] = course.xpath('div[1]/h3/a/text()').extract_first().strip()
            item['update_time'] = course.xpath('div[3]/relative-time/@datetime').extract_first()
            course_url = response.urljoin(course.xpath('div[1]/h3/a/@href').extract_first())
            request = scrapy.Request(course_url,callback=self.parse_author)
            request.meta['item'] = item
            yield request

    def parse_author(self, response):
        item = response.meta['item']
        item['commits'] = response.xpath('//*[@class="numbers-summary"]/li[1]/a/span/text()').extract_first(default='0').strip().replace(',','')
        item['branches'] = response.xpath('//*[@class="numbers-summary"]/li[2]/a/span/text()').extract_first(default='0').strip().replace(',','')
        item['releases'] = response.xpath('//*[@class="numbers-summary"]/li[3]/a/span/text()').extract_first(default='0').strip().replace(',','')
        yield item