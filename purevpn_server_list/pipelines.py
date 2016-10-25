# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from util import cleanup

class PurevpnServerListPipeline(object):
    def open_spider(self, spider):
        import os
        cleanup(os.path.join('templates', 'data.json'))

    def process_item(self, item, spider):
        item.update({key: value[0] for key, value in item.iteritems()})
        item.update({key: value.upper() for key, value in item.iteritems() if key in ['region', 'country', 'city']})
        return item
