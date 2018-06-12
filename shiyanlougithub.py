# -*- coding:utf-8 -*-
import scrapy
import json

class ShiyanlouCoursesSpider(scrapy.Spider):
    name = 'shiyanlou-github'

    def start_requests(self):
        url_tmpl='https://github.com/shiyanlou?page={}&tab=repositories'
        urls = (url_tmpl.format(i) for i in range(1, 5))
        for url in urls:
            print('********', url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for course in response.xpath('//li[@class="col-12 d-block width-full py-4 border-bottom public source"]'):
            yield {
                'name':course.xpath('div[@class="d-inline-block mb-1"]/h3/a/text()').extract_first().strip(),
                'update_time': course.xpath('div[@class="f6 text-gray mt-2"]/relative-time/@datetime').extract_first().strip()

            }

        for course in response.xpath('//li[@class="col-12 d-block width-full py-4 border-bottom public fork"]'):
            yield {
                'name':course.xpath('div[@class="d-inline-block mb-1"]/h3/a/text()').extract_first().strip(),
                'update_time': course.xpath('div[@class="f6 text-gray mt-2"]/relative-time/@datetime').extract_first().strip()

            }
