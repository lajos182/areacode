# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json

class AreacodePipeline(object):

    # 重写这个方法，当爬虫开启的时候就会调用这个方法
    def open_spider(self, spider):
        self.fp = open('./areacode/spiders/area.txt', 'w', encoding='utf-8')

    # 处理item数据的方法，该方法是重写方法
    def process_item(self, item, spider):
        # 要将item保存到文件中
        # 将对象转化为字典
        dt = dict(item)
        dt_string = json.dumps(dt, ensure_ascii=False)
        self.fp.write(dt_string + '\n')
        return item

    # 重写这个方法，当爬虫结束的时候就会调用这个方法
    def close_spider(self, spider):
        self.fp.close()