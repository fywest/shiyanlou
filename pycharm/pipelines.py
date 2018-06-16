# -*- coding: utf-8 -*-
# Define your item pipelines here
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from datetime import datetime
from sqlalchemy.orm import sessionmaker
from .models import Repository,engine
from scrapy.exceptions import DropItem
from .items import RepositoryItem

class ShiyanlouPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, RepositoryItem):
            self._process_repository_item(item)

        return item

    def _process_repository_item(self, item):
        item['update_time'] = datetime.strptime(item['update_time'].split()[0], '%Y-%m-%dT%H:%M:%SZ')
        item['commits'] = int(item['commits'])
        item['branches'] = int(item['branches'])
        item['releases'] = int(item['releases'])
        self.session.add(Repository(**item))
    
    def open_spider(self, spider):
        Session = sessionmaker(bind=engine)
        self.session = Session()
                                                        
    def close_spider(self, spider):
        self.session.commit()
        self.session.close()
