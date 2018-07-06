# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeiboredisspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class UserInfoItem(scrapy.Item):

    crawled = scrapy.Field()
    spider = scrapy.Field()

    mtype = scrapy.Field()

    # 以下信息在json串中的data -- userinfo字段
    uid = scrapy.Field()
    screen_name = scrapy.Field()
    profile_image_url = scrapy.Field()
    profile_url = scrapy.Field()
    statuses_count = scrapy.Field()
    # 是否是认证用户 true  false
    verified = scrapy.Field()
    # 认证类型， -1 为没认证。0为个人认证，其余为企业认证
    verified_type = scrapy.Field()
    # _ext为1时(橙色V)， _ext为0（黄色v）
    # verified_type_ext = scrapy.Field()
    # 认证说明
    verified_reason = scrapy.Field()
    # close_blue_v = scrapy.Field()
    # 简介
    description = scrapy.Field()
    # f为女，m为男
    gender = scrapy.Field()
    # 等级
    urank = scrapy.Field()
    # 会员等级
    mbrank = scrapy.Field()
    # 是否关注我
    follow_me = scrapy.Field()
    # 我是否关注他
    following = scrapy.Field()
    # 粉丝数量
    followers_count = scrapy.Field()
    # 关注量
    follow_count = scrapy.Field()

    # 以下4个信息必须记录
    # 在 data -- fans_scheme字段
    fans_scheme = scrapy.Field()
    # 在 data -- fans_scheme字段
    follow_scheme = scrapy.Field()
    # tabsInfo -- tabs -- 0 -- containerid
    profile_containerid = scrapy.Field()
    # tabsInfo -- tabs -- 1 -- containerid
    weibo_containerid = scrapy.Field()


class WeiboInfoItem(scrapy.Item):

    crawled = scrapy.Field()
    spider = scrapy.Field()

    mtype = scrapy.Field()

    # 用户uid
    uid = scrapy.Field()
    # 创建时间
    created_at = scrapy.Field()
    # 存储id
    mid = scrapy.Field()
    # 是否可编辑
    can_edit = scrapy.Field()
    # 微博内容，含html
    text = scrapy.Field()
    # 微博长度
    textLength = scrapy.Field()
    # 发表来源（如iPhone 6）
    source = scrapy.Field()
    # 是否已收藏，true：是，false：否
    favorited = scrapy.Field()
    # 微博配图ID。多图时返回多图ID，用来拼接图片url。用返回字段thumbnail_pic的地址配上该返回字段的图片ID，即可得到多个图片url。
    pic_ids = scrapy.Field()

    # 图片缩略图地址，没有图片则无此字段
    thumbnail_pic = scrapy.Field()
    is_paid = scrapy.Field()
    mblog_vip_type = scrapy.Field()

    # 转发了别人的微博，否则无此字段
    # retweeted_status = scrapy.Field()
    is_retweeted = scrapy.Field()

    # 转发数
    reposts_count = scrapy.Field()
    # 评论数
    comments_count = scrapy.Field()
    # 表态数
    attitudes_count = scrapy.Field()

    pending_approval_count = scrapy.Field()
    # 是否是长文本  true false
    isLongText = scrapy.Field()
    # 微博的可见性及指定可见分组信息。该object中type取值，0：普通微博，1：私密微博，3：指定分组微博，4：密友微博；list_id为分组的组号
    # visible = scrapy.Field()
    visible_type = scrapy.Field()
    visible_list_id = scrapy.Field()

    more_info_type = scrapy.Field()
    content_auth = scrapy.Field()

    # 页面信息，视频video或者图片 或者话题topic 或者地点place
    page_info = scrapy.Field()
    page_info_type = scrapy.Field()
    page_info_title = scrapy.Field()
    page_info_content1 = scrapy.Field()
    page_info_content2 = scrapy.Field()

    # 图片详细信息，数组，包括pid,url,size,geo
    pics = scrapy.Field()


class WeiboUIDItem(scrapy.Item):
    mtype = scrapy.Field()

    crawled = scrapy.Field()
    spider = scrapy.Field()
    uid = scrapy.Field()
