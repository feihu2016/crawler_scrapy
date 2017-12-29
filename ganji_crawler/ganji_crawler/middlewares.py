# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
from agents import AGENTS
import random
from config import DB_SERVER, DB_CONNECT
from helpers import *
from log import *

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from scrapy.http import HtmlResponse

from scrapy import signals


class GanjiCrawlerSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


def free_proxy():
    pass
    #db = SimpleMysql(**DB_CONNECT)
    #date_where = whichday(-1)
    #return db.getAll(table='free_proxy_list',
    #    where = ("last_checked > %s AND checked_status = %s AND https = 'HTTP' ", [date_where, "1"]),
    #    order = ('last_checked', 'DESC'),
    #    limit = (0, 1000)
    #)

FREE_PROXIES_FROMDB = free_proxy()

def random_proxy():
    if FREE_PROXIES_FROMDB:
        length = len(FREE_PROXIES_FROMDB)
        index  = random.choice(range(0,length))
        p = FREE_PROXIES_FROMDB[index]
        ip_port = "%s:%s" % (p.ip, p.port)
        return ip_port

class CustomHttpProxyFromMysqlMiddleware(object):
    def process_request(self, request, spider):
        if self.use_proxy(request):
            try:
                ip_port = random_proxy()
                if not ip_port:
                    debug("CustomHttpProxyFromMysqlMiddleware: empty proxy pool.")
                    return
                request.meta['proxy'] = "http://%s" % ip_port
                debug("CustomHttpProxyFromMysqlMiddleware proxy:" + request.meta['proxy'])
            except Exception, e:
                print e

    def use_proxy(self, request):
        """
        using direct download for depth <= 2
        using proxy with probability 0.3
        """
        #if "depth" in request.meta and int(request.meta['depth']) <= 2:
        #    return False
        #i = random.randint(1, 10)
        #return i <= 2
        return True


class CustomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        agent = random.choice(AGENTS)
        debug(request.url + "\t\tCustomUserAgentMiddleware: " + agent )
        request.headers['User-Agent'] = agent


class CustomJavaScriptMiddleware(object):
    def process_request(self, request, spider):
        debug("PhantomJS is starting...")
        try:
            dcap = dict(DesiredCapabilities.PHANTOMJS)
            dcap["phantomjs.page.settings.resourceTimeout"] = 5  # 超时
            dcap["phantomjs.page.settings.loadImages"] = False
            # 伪造ua信息
            dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36")
            # 添加头文件
            dcap["phantomjs.page.customHeaders.Referer"] = (
               "https://www.google.com.hk/#newwindow=1&safe=strict&q=%E5%AE%89%E5%B1%85%E5%AE%A2"
            )
            # 代理
            service_args = [
                # '--proxy=127.0.0.1:8080',
                #'--proxy-type=http',
                #'--proxy-type=socks5',
                #'--proxy-auth=username:password'
            ]
            #指定使用的浏览器
            driver = webdriver.PhantomJS(
                # executable_path='/usr/bin/phantomjs',
                # executable_path='phantomjs',
                # service_args=service_args,
                desired_capabilities=dcap
            )
            driver.set_window_size(1400,1000)
            driver.get(request.url)
            # time.sleep(1)
            # js = "var q=document.documentElement.scrollTop=10000"
            # driver.execute_script(js) #可执行js，模仿用户操作。此处为将页面拉至最底端。
            time.sleep(3)
            body = driver.page_source
            debug("访问"+request.url)
            url = driver.current_url
            driver.close()
            return HtmlResponse(url, body=body, encoding='utf-8', request=request)
        except Exception as e:
            driver.close()
            print e
