# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GanjiCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class JJRItem(scrapy.Item):
    """
    姓名、电话、公司名称（示例网址： http://sh.ganji.com/fang_1720020/）
    """
    info_id = scrapy.Field()
    url = scrapy.Field()
    agent_name = scrapy.Field()
    phone = scrapy.Field()
    company = scrapy.Field()
    company_url = scrapy.Field()
    serv_type = scrapy.Field()


class HouseItem(scrapy.Item):
    """
    写字楼出租
    """
    house_id = scrapy.Field()  # bigint(20)  '房源id ', ++++++
    created_at = scrapy.Field() # int(10)  '首次入库时间', +++++
    updated_at = scrapy.Field() # int(10) '最后更新时间', ++++++
    crawled_at = scrapy.Field() # date  '最后抓取批次日期', +++++
    url = scrapy.Field() # varchar(500) '爬取url',   ---------
    area = scrapy.Field() # decimal(8,2)'面积', --------
    rent_price = scrapy.Field() # decimal(8,2) '价格', --------
    rent_price_unit = scrapy.Field() # varchar(50) '价格单位', +++++
    guwen = scrapy.Field() # varchar(50) '联系人',-------|||||||
    guwen_phone = scrapy.Field() # varchar(50) '电话'---------||||||

    title = scrapy.Field() #  varchar(255) '标题', 
    pub_date = scrapy.Field() #` varchar(20) '发布时间',
    city_id = scrapy.Field() # int(10) '城市id',          
    city_name = scrapy.Field() # varchar(20) '城市名称',
   
    district_name = scrapy.Field() # varchar(50) '区域', ----- 
    district_pinyin = scrapy.Field() # varchar(50) '区域拼音',

    street_name = scrapy.Field() # varchar(50)'商圈',  ------- 
    street_pinyin = scrapy.Field() # varchar(50) '商圈拼音',
    address = scrapy.Field() # varchar(100) '地段', -------     
    building_name = scrapy.Field() # varchar(50) '楼盘',----- 
    userage = scrapy.Field() # int(4) '账号年限',---------
    company = scrapy.Field() # varchar(100)  '所属公司',------

    
    istop = scrapy.Field() # int(1) '是否置顶', 
    iscream = scrapy.Field() # int(1) '是否精华', 
    info_type = scrapy.Field() # int(1)  '类别 1出租 2求租 3出售 4求购', 
    company_url = scrapy.Field() # varchar(500)  '商铺url', ++++++
    

