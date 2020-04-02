# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import pymysql
import requests


class HousepriceSpiderMiddleware(object):
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

        # Should return either None or an iterable of Request, dict
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


class HousepriceDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


conf = {
    'host': 'dev.finlu.com.cn',
    'port': 3306,
    'user': 'admin',
    'password': 'mysqlvip',
    'db_name': 'ip_proxy'
}
import time

class RandomUserAgent:
    def get_headers(self):
        return 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'

class MyproxiesSpiderMiddleware(object):

    def __init__(self):
        self.target_url = 'http://httpbin.org/get'
        self.target_url_https = 'https://httpbin.org/get'
        try:
            conn = pymysql.Connect(host=conf['host'], port=conf['port'], user=conf['user'], password=conf['password'],
                                   db=conf['db_name'], charset='utf8')
            self.cursor = conn.cursor()
            sql = """SELECT ip_addr, area_addr, port, https, post, speed from ip_aboard order by speed"""
            self.cursor.execute(sql)
            self.ip_proxies = list(self.cursor.fetchall())

        except Exception as e:
            print('数据库连接异常', e)
        finally:
            self.cursor.close()
    def check_ip(self, proxy):
        try:
            randomUserAgent = RandomUserAgent()
            r = requests.get(url=self.target_url, headers=randomUserAgent.get_headers(), timeout=5,
                             proxies=proxy)
            if r.ok:
                return True
            else:
                return False
        except Exception as e:
            return False


    def process_request(self, request, spider):
        for ip_info in self.ip_proxies:
            proxy  = {"http": "http://%s:%s" % (ip_info[0], ip_info[2]), "https": "http://%s:%s" % (ip_info[0], ip_info[2])}
            if self.check_ip(proxy):
                request.meta["proxy"] = proxy["http"]
                break
        self.ip_proxies