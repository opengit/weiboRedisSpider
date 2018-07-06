# -*- coding: utf-8 -*-
import scrapy
import json
import re
import time
from scrapy_redis.spiders import RedisSpider
from scrapy.conf import settings
from weiboRedisSpider.items import UserInfoItem, WeiboInfoItem, WeiboUIDItem
from weiboRedisSpider.mytools import convert_timestamp


class WeiboSpider(RedisSpider):
    name = 'weibo'

    # 获取用户信息json的api
    user_api_url = "https://m.weibo.cn/api/container/getIndex?type=uid&value={uid}"
    # 获取微博信息json的api
    weibo_api_url = "https://m.weibo.cn/api/container/getIndex?containerid=107603{uid}&page={page}"
    # 获取粉丝列表json的api
    fans_api_url = "https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_{uid}&page={page}"
    # 获取关注列表json的api
    followers_api_url = "https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_{uid}&page={page}"

    # 粉丝、关注爬虫深度（页数），越大扩散范围越广
    fans_followers_depth = settings['FANS_FOLLOWERS_DEPTH']
    # 设置微博最后时间，当前时间2018-06-08 00:00:00
    weibo_deadline = settings['WEIBO_DEADLINE']

    # 用于接收redis发送的爬取命令
    redis_key = "weibospider:start_urls"

    # 【测试用】
    # https://m.weibo.cn/api/container/getIndex?type=uid&value=3781960940   # suprsvn
    # https://m.weibo.cn/api/container/getIndex?type=uid&value=5082883214   # AndroidTips
    # https://m.weibo.cn/api/container/getIndex?type=uid&value=6211974038   # gitopen

    # 【正式用】
    # https://m.weibo.cn/api/container/getIndex?type=uid&value=1243861097   # 【李想】 汽车之家
    # https://m.weibo.cn/api/container/getIndex?type=uid&value=5016338752   # 【郑州大学】 官方微博
    # https://m.weibo.cn/api/container/getIndex?type=uid&value=1734530730   # 【大河报】 官方微博

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(WeiboSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        '''
        解析用户信息
        '''
        print("*" * 10, "parse开始执行...")

        # 解析信息
        user_dict = json.loads(response.text)
        user_info = user_dict['data']['userInfo']
        # print("*" * 10, user_dict)

        user_info_item = UserInfoItem()
        user_info_item['mtype'] = "user"
        user_info_item['uid'] = user_info['id']
        user_info_item['screen_name'] = user_info['screen_name']
        user_info_item['profile_image_url'] = user_info['profile_image_url']
        user_info_item['profile_url'] = user_info['profile_url']
        user_info_item['statuses_count'] = user_info['statuses_count']
        user_info_item['verified'] = user_info['verified']
        user_info_item['verified_type'] = user_info['verified_type']
        # 可能不存在
        # userInfoItem['verified_type_ext'] = "" if user_info['verified_type'] == -1 else user_info['verified_type_ext']
        user_info_item['verified_reason'] = user_info['verified_reason'] if "verified_reason" in user_info.keys() \
            else ""
        # userInfoItem['close_blue_v'] = user_info['close_blue_v']
        user_info_item['description'] = user_info['description']
        user_info_item['gender'] = user_info['gender']
        user_info_item['urank'] = user_info['urank']
        user_info_item['mbrank'] = user_info['mbrank']
        user_info_item['follow_me'] = user_info['follow_me']
        user_info_item['following'] = user_info['following']
        user_info_item['followers_count'] = user_info['followers_count']
        user_info_item['follow_count'] = user_info['follow_count']

        user_info_item['fans_scheme'] = user_dict['data']['fans_scheme']
        user_info_item['follow_scheme'] = user_dict['data']['follow_scheme']
        user_info_item['profile_containerid'] = user_dict['data']['tabsInfo']['tabs'][0]['containerid']
        user_info_item['weibo_containerid'] = user_dict['data']['tabsInfo']['tabs'][1]['containerid']

        print("*" * 10, "当前解析用户为【{}】...".format(user_info_item['screen_name']))

        yield user_info_item

        # 发送微博处理请求
        uid = user_info_item['uid']
        # 10829/10 = 1082.9
        # 1082 + 2 = 1084
        total_pages = int(user_info_item['statuses_count'] / 10) + 2
        for page in range(1, total_pages + 1):
            yield scrapy.Request(self.weibo_api_url.format(uid=uid, page=page), callback=self.parse_weibos, priority=5)
            # yield scrapy.Request(self.weibo_api_url.format(uid=uid, page=page), callback=self.parse_weibos)

        # 发送处理粉丝和关注请求
        for page in range(self.fans_followers_depth + 1):
            # yield scrapy.Request(self.followers_api_url.format(uid=uid, page=page), callback=self.parse_fans_followers,priority=4)
            yield scrapy.Request(self.fans_api_url.format(uid=uid, page=page), callback=self.parse_fans_followers,
                                 priority=4)

        print("*" * 10, "parse结束执行...")

    def parse_weibos(self, response):
        '''
        从微博json中拿到weibo_scheme
        '''
        print("*" * 10, "parse_weibos开始执行...")

        weibos_dict = json.loads(response.text)
        # print(weibos_dict)
        cards = weibos_dict['data']['cards']
        # 根据page迭代的时候，有的page不准确，会出现json中cards列表长度为0的情况，这时scrapy报错，所以判断一下
        if len(cards) > 0:
            for card in cards:
                # 如果当前迭代的数据处于微博json的第1页，那么cards中有一些card不含有mblog字段，因此需要过滤
                if 'mblog' in card.keys():
                    created_at = card['mblog']['created_at']
                    created_at_list = str(created_at).split("-")
                    # 处理一下时间格式为01-12
                    if len(created_at_list) == 2:
                        created_at = "2018-" + card['mblog']['created_at'] + " 00:00:00"
                    # 处理一下时间格式为2017-12-20
                    elif len(created_at_list) == 3:
                        created_at = card['mblog']['created_at'] + " 00:00:00"
                    # 其他格式，例如 xx分钟前，xxx小时前，统一设置为当前时间，让它通过，交给parse_weibo_status处理
                    else:
                        created_at = time.strftime('%Y-%m-%d %H:%M:%S')

                    # 只有当此微博的时间在设定的最后时限之前，才符合抓取要求
                    if convert_timestamp(created_at) < convert_timestamp(self.weibo_deadline):
                        print("*" * 10, "时间为【{}】的微博被抛弃...".format(created_at))
                    else:
                        # 因为有的card中没有scheme，需要判断，不然scrapy会报错
                        if "scheme" in card.keys():
                            weibo_scheme = card['scheme']
                            yield scrapy.Request(url=weibo_scheme, callback=self.parse_weibo_status, priority=6)

        print("*" * 10, "parse_weibos结束执行...")

    def parse_weibo_status(self, response):
        '''
        解析微博数据。
        从访问weibo_scheme页面的响应数据中，用正则匹配出weibo_status的json，才是真正要的微博数据。
        '''
        print("*" * 10, "parse_weibo_status开始执行...")

        # 当html页面中有$render_data字符串，说明单条微博，也就是status页面加载成功，才能解析
        if '$render_data' not in response.text:
            print("*" * 10, "页面没有【$render_data】数据被跳过...")
        else:
            # 1. 用正则表达式从response.body中拿出json字符串
            r = re.compile(r'var \$render_data(.|\n)*{};')
            result = r.search(str(response.text)).group()
            json_str = result.replace("var $render_data = [", "").replace("][0] || {};", "")

            # 2. 将json字符串转化为dict
            weibo_dict = json.loads(json_str)

            # 3. 获取status字典
            weibo_status = weibo_dict["status"]
            created_at = time.strftime("%Y-%m-%d %H:%M:%S",
                                       time.strptime(weibo_status["created_at"].replace("+0800", "")))
            print("*" * 10, "时间为【{}】的微博被抓取...".format(created_at))
            # 4. 提取数据到item
            weibo_info_item = WeiboInfoItem()
            weibo_info_item['mtype'] = "weibo"
            # 拿出来的时间是Mon Jan 16 12:55:58 +0800 2017，将其格式化为2017-01-16 12:55:58
            weibo_info_item['created_at'] = created_at
            weibo_info_item['uid'] = weibo_status["user"]["id"]
            weibo_info_item['mid'] = weibo_status["mid"]
            weibo_info_item['can_edit'] = weibo_status["can_edit"]
            weibo_info_item['text'] = weibo_status["text"]

            weibo_info_item['textLength'] = weibo_status["textLength"] \
                if "textLength" in weibo_status.keys() else -1
            weibo_info_item['source'] = weibo_status["source"]
            weibo_info_item['favorited'] = weibo_status["favorited"]
            # 列表长度可能为0
            weibo_info_item['pic_ids'] = weibo_status["pic_ids"]
            # 可能不存在
            weibo_info_item['thumbnail_pic'] = weibo_status["thumbnail_pic"] \
                if "thumbnail_pic" in weibo_status.keys() else ""
            weibo_info_item['is_paid'] = weibo_status["is_paid"]
            weibo_info_item['mblog_vip_type'] = weibo_status["mblog_vip_type"]
            # 如果是转发微博，true
            weibo_info_item['is_retweeted'] = True \
                if "retweeted_status" in weibo_status.keys() else False
            weibo_info_item['reposts_count'] = weibo_status["reposts_count"]
            weibo_info_item['comments_count'] = weibo_status["comments_count"]
            weibo_info_item['attitudes_count'] = weibo_status["attitudes_count"]
            weibo_info_item['pending_approval_count'] = weibo_status["pending_approval_count"]
            weibo_info_item['isLongText'] = weibo_status["isLongText"]
            weibo_info_item['visible_type'] = weibo_status["visible"]["type"]
            weibo_info_item['visible_list_id'] = weibo_status["visible"]["list_id"]
            weibo_info_item['more_info_type'] = weibo_status["more_info_type"]
            weibo_info_item['content_auth'] = weibo_status["content_auth"]
            # page_info可能不存在
            if "page_info" in weibo_status.keys():
                weibo_info_item['page_info'] = weibo_status["page_info"]
                weibo_info_item['page_info_type'] = weibo_status["page_info"]["type"]
                weibo_info_item['page_info_title'] = weibo_status["page_info"]["page_title"]
                weibo_info_item['page_info_content1'] = weibo_status["page_info"]["content1"]
                weibo_info_item['page_info_content2'] = weibo_status["page_info"]["content2"] \
                    if 'content2' in weibo_status["page_info"].keys() else ""
            # pics列表，可能不存在
            weibo_info_item['pics'] = weibo_status["pics"] \
                if "pics" in weibo_status.keys() else []

            # 5. 将item交给管道文件处理
            yield weibo_info_item

        print("*" * 10, "parse_weibo_status结束执行...")

    def parse_fans_followers(self, response):
        '''
        拿到fan或者follow的uid，用于迭代。
        '''
        print("*" * 10, "parse_fans_followers开始执行...")

        json_dict = json.loads(response.body)
        cards_root = json_dict["data"]["cards"]
        if len(cards_root) > 0:
            cards_follow = cards_root[-1]
            card_group = cards_follow['card_group']
            for card in card_group:
                user_info = card['user']
                uid = user_info['id']

                uid_item = WeiboUIDItem()
                uid_item['mtype'] = "uid"
                uid_item['uid'] = uid
                yield uid_item

                user_url = self.user_api_url.format(uid=str(uid))
                yield scrapy.Request(url=user_url, callback=self.parse, priority=5)

        print("*" * 10, "parse_fans_followers结束执行...")
