# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from weiboRedisSpider.items import UserInfoItem, WeiboInfoItem, WeiboUIDItem
from weiboRedisSpider.mytools import write_parsed_json_data_to_file, write_raw_data_to_file
import time
from scrapy.conf import settings
import pymongo


class WeiboredisspiderPipeline(object):

    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbname = settings['MONGODB_DB_NAME']

        self.sheet_user = settings['MONGODB_SHEET_USER']
        self.sheet_weibo = settings['MONGODB_SHEET_WEIBO']
        self.sheet_uid = settings['MONGODB_SHEET_UID']

        client = pymongo.MongoClient(host=host, port=int(port))
        self.mydb = client[dbname]

        self.is_write = settings['WRITE_TO_FILE']
        self.machine_name = settings['MACHINE_NAME']

    def process_item(self, item, spider):

        item["crawled"] = time.strftime('%Y-%m-%d %H:%M:%S')
        item["spider"] = spider.name + "-" + self.machine_name

        if isinstance(item, UserInfoItem):
            print("*" * 10, "WbspiderPipeline --> process_item正在处理UserInfoItem...")

            self.mydb[self.sheet_user].insert_one(dict(item))
            if self.is_write:
                write_parsed_json_data_to_file(item, "./result_3_year/user_data/result_parse.json")

            print("*" * 10, "WbspiderPipeline --> process_item结束处理UserInfoItem...")
        elif isinstance(item, WeiboInfoItem):
            print("*" * 10, "WbspiderPipeline --> process_item正在处理WeiboInfoItem...")

            self.mydb[self.sheet_weibo].insert_one(dict(item))
            if self.is_write:
                write_parsed_json_data_to_file(item, "./result_3_year/weibo_data/result_parse.json")

            print("*" * 10, "WbspiderPipeline --> process_item结束处理WeiboInfoItem...")
        elif isinstance(item, WeiboUIDItem):
            print("*" * 10, "WbspiderPipeline --> process_item正在处理WeiboUIDItem...")

            self.mydb[self.sheet_uid].insert_one(dict(item))
            if self.is_write:
                write_parsed_json_data_to_file(item, "./result_3_year/all_uid/result_parse.json")

            print("*" * 10, "WbspiderPipeline --> process_item结束处理WeiboInfoItem...")

        return item
