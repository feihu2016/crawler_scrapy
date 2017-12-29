#-*- coding: utf-8 -*-

import scrapy,re,sys,time

from scrapy.http import Request
from ganji_crawler.items import HouseItem
from ganji_crawler.log import *
from ganji_crawler.helpers import *
from ganji_crawler.rules import rules_qiuzu


class qiuzuspiderSpider(scrapy.Spider):
    name = "qiuzu"
    allowed_domains = ["ganji.com"]
    start_urls = [
        "http://bj.ganji.com/fang8/s2/_%E6%B1%82%E7%A7%9F/",
        "http://cd.ganji.com/fang8/s2/_%E6%B1%82%E7%A7%9F/",
        "http://dl.ganji.com/fang8/s2/_%E6%B1%82%E7%A7%9F/",
        "http://gz.ganji.com/fang8/s2/_%E6%B1%82%E7%A7%9F/",
        "http://hz.ganji.com/fang8/s2/_%E6%B1%82%E7%A7%9F/",
        "http://sh.ganji.com/fang8/s2/_%E6%B1%82%E7%A7%9F/",
        "http://sz.ganji.com/fang8/s2/_%E6%B1%82%E7%A7%9F/",
        "http://tj.ganji.com/fang8/s2/_%E6%B1%82%E7%A7%9F/",
        "http://wh.ganji.com/fang8/s2/_%E6%B1%82%E7%A7%9F/",
        "http://xa.ganji.com/fang8/s2/_%E6%B1%82%E7%A7%9F/"
    ]

    def parse(self, response):
        #if re.match('.*callback\.ganji\.com', response.url):
        list_url = response.xpath(rules_qiuzu.get('house_list')).extract()
        host_url = response.url[0:response.url.index('.com')+4]
        for url in list_url:
            request_url = host_url + url
            yield Request(request_url, meta={'referer':response.url}, callback=self.content_parse)

        data_next_page = retstr_replace(response.xpath(rules_qiuzu.get('house_list_nextpage')).extract())
        #data_next_page = False
        if data_next_page:
            data_next_page = host_url + data_next_page
            yield Request(data_next_page, meta={'referer':response.url}, callback=self.parse)

    def content_parse(self, response):
        item = HouseItem()
        item['house_id'] = 0
        item['url'] = response.url
        item['created_at'] = date_timestamp()
        item['updated_at'] = date_timestamp()
        item['crawled_at'] = date_today()

        html_lists = response.xpath(rules_qiuzu.get('path_list')).extract()
        item['rent_price'] = 0
        item['rent_price_unit'] = ''
        item['area'] = 0
        item['company'] = ''
        item['district_name'] = ''
        item['street_name'] = ''
        item['address'] = ''
        for html in html_lists:
            if html.find(u'租')>0 and html.find(u'金')>0:
                result = re.findall(r'<b .*>(\d+)</b>(.*)',html)
                if result:
                    item['rent_price'] = result[0][0]
                    item['rent_price_unit'] = result[0][1] if len(result[0])>1 else ''
            elif html.find(u'面')>0 and html.find(u'积')>0:
                result = re.findall(u'(\d+)㎡',html)
                item['area'] = result[0] if result else 0
            elif html.find(u'类')>0 and html.find(u'型')>0:
                result = re.findall(r'<a .*>(.*)</a>',html)
                item['company'] = result[0] if result else ''                
            elif html.find(u'区')>0 and html.find(u'域')>0:
                result = re.findall(r'<a .*?>(.*?)</a>',html)
                if result:
                    item['district_name'] = result[1] if len(result)>1 else ''
                    item['street_name'] = result[2] if len(result)>2 else ''
                else:
                    item['district_name'] = ''
                    item['street_name'] = ''
            elif html.find(u'地')>0 and html.find(u'址')>0:
                result = re.findall('<span title=.*?>(.*?)</span>',html)
                item['address'] = result[0] if result else ''
        
        item['company_url'] = retstr_replace(response.xpath(rules_qiuzu['isperson']).extract())
        if len(item['company_url'])>2:
            item['company_url'] = item['company_url'][0:2]
        item['guwen'] = retstr_replace(response.xpath(rules_qiuzu['guwen']).extract())
        item['guwen_phone'] = retstr_replace(response.xpath(rules_qiuzu['guwen_phone']).extract()).replace(' ', '')
        item['userage'] = retstr_replace(response.xpath(rules_qiuzu['click_num']).extract())
        item['building_name'] = retstr_replace(response.xpath(rules_qiuzu['building_name']).extract())
       
        cityinfo  = cityInfo(self.getDomain(response.url))
        item['city_id'] = cityinfo['city_id']
        item['city_name'] = cityinfo['city_name']

        item['district_pinyin'] = ''
        item['street_pinyin'] = ''

        item['pub_date'] =  retstr_replace(response.xpath(rules_qiuzu['pub_date']).extract())
        item['title'] = retstr_replace(response.xpath(rules_qiuzu['title']).extract())
        item['istop'] = 0
        item['iscream'] = 0
        item['info_type'] = self.getInfoType(item['title'])
        yield item  

    def getInfoType(self, title_str):
        """
        1出租 2求租 3出售 4求购 
        """
        if title_str.find(u'出租')>=0:
            return 1
        elif title_str.find(u'求租')>=0:
            return 2
        elif title_str.find(u'出售')>=0:
            return 3
        elif title_str.find(u'求购')>=0:  
            return 4
        else:
            return 0

    def getDomain(self, url):
        return re.search(r'(\w+).ganji.com', url).group(1)
