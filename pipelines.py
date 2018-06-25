# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class DoubanMoviePipeline(object):
#     def process_item(self, item, spider):
#         return item

# todo

import re
import redis
import json
from scrapy.exceptions import DropItem


class DoubanMoviePipeline(object):
    def process_item(self, item, spider):
        item['summary'] = re.sub('\s+', ' ', item['summary'])
        if not float(item['score']) >= 8.0:
            raise DropItem('score less than 8.0')
        self.redis.lpush('douban_movie:items', json.dumps(dict(item)))
        return item

    def open_spider(self, spider):
        self.redis = redis.StrictRedis(host='localhost', port=6379, db=0)