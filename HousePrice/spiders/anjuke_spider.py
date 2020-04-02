# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from HousePrice.items import ErShouFangSourceItem, RentingHouseSourceItem
from utils import decrypt_text
import re

class AnjukeSpider(scrapy.Spider):
    name = 'anjuke_spider'
    allowed_domains = ['anjuke.com']
    start_urls = ['https://guangzhou.anjuke.com/sale/t18/']

    def __init__(self, name=None, **kwargs):
        super().__init__(name=name, **kwargs)
        self.test = True
        self.city_area_info = {
            'beijing': {
                'chaoyang': '朝阳区',
                'haidian': '海淀区',
                # 'dongchenga': '东城区',
                # 'xicheng': '西城区',
                # 'tongzhou': '通州区',
                # 'shunyi': '顺义区'
            },
            # 'guangzhou': {
            #     'tianhe': '天河区',
            #     'fanyu': '番禺区',
            #     'haizhu': '海珠区',
            #     'huangpua': '黄埔区',
            #     'nansha': '南沙区',
            #     'yuexiu': '越秀区',
            #     'liwan': '荔湾区',
            #     'baiyun': '白云区',
            # },
            # 'shenzhen': {
            #     'longgang': '龙岗区',
            #     'nanshan': '南山区',
            #     'baoan': '宝安区',
            #     'futian': '福田区',
            #     'longhuaq': '龙华区',
            #     'luohu': '罗湖区',
            #     'bujisz': '布吉',
            #     'yantian': '盐田区',
            #     'guangmingx': '光明区',
            #     'pingshanq': '坪山区',
            #     'shenzhenzhoubian': '深圳周边'
            # }
        }
        self.zufang_city_area_info = {
            'bj': {
                'chaoyang': '朝阳区',
                'haidian': '海淀区',
                # 'dongchenga': '东城区',
                # 'xicheng': '西城区',
                # 'tongzhou': '通州区',
                # 'shunyi': '顺义区'
            },
            # 'gz': {
            #     'tianhe': '天河区',
            #     'fanyu': '番禺区',
            #     'haizhu': '海珠区',
            #     'huangpua': '黄埔区',
            #     'nansha': '南沙区',
            #     'yuexiu': '越秀区',
            #     'liwan': '荔湾区',
            #     'baiyun': '白云区',
            # },
            # 'sz': {
            #     'longgang': '龙岗区',
            #     'nanshan': '南山区',
            #     'baoan': '宝安区',
            #     'futian': '福田区',
            #     'longhuaq': '龙华区',
            #     'luohu': '罗湖区',
            #     'bujisz': '布吉',
            #     'yantian': '盐田区',
            #     'guangmingx': '光明区',
            #     'pingshanq': '坪山区',
            #     'shenzhenzhoubian': '深圳周边'
            # }
        }
        self.city_map = {
            'beijing': 'bj',
            'guangzhou': 'gz',
            'shenzhen': 'sz'
        }

    def start_requests(self):
        # 二手房
        for city, area_info in self.city_area_info.items():
            for area_code, area_name in self.city_area_info[city].items():
                url = 'https://{}.anjuke.com/sale/{}/'.format(city, area_code)
                yield Request(url=url, callback=self.parse_shangquan,
                              cb_kwargs={'city': city, 'area': area_name, 'type': 'ershoufang'},
                              dont_filter=True)
        # 租房
        for city, area_info in self.zufang_city_area_info.items():
            for area_code, area_name in self.zufang_city_area_info[city].items():
                url = 'https://{}.zu.anjuke.com/fangyuan/{}/'.format(city, area_code)
                yield Request(url=url, callback=self.parse_shangquan, cb_kwargs={'city': city, 'area': area_name, 'type': 'zufang'},
                              dont_filter=True)

    def parse_shangquan(self, response, **kwargs):
        """
        获取所有的商圈信息
        :param response:
        :param kwargs:
        :return:
        """
        info_type = kwargs.get('type')
        if info_type == 'ershoufang':
            shangquan_node_list = response.css('div.sub-items a')
            if self.test:
                shangquan_node_list = shangquan_node_list[:1]
            for shangquan_node in shangquan_node_list:
                url = shangquan_node.attrib.get('href')
                kwargs.update({
                    'business_circle': shangquan_node.css('::text').get(default='')
                })
                yield Request(url=url, callback=self.parse, cb_kwargs=kwargs)
        elif info_type == 'zufang':
            shangquan_node_list = response.css('div.sub-items.sub-level2 a')[1:]
            if self.test:
                shangquan_node_list = shangquan_node_list[:1]
            for shangquan_node in shangquan_node_list:
                url = shangquan_node.attrib.get('href')
                kwargs.update({
                    'business_circle': shangquan_node.css('::text').get(default='')
                })
                yield Request(url=url, callback=self.parse, cb_kwargs=kwargs)
    def parse(self, response, **kwargs):
        """
        跳转到列表详情并翻页
        :param response:
        :param kwargs:
        :return:
        """
        info_type = kwargs.get('type')
        if info_type == 'ershoufang':
            detail_link_node_list = response.css('.houselist-mod-new .house-details .house-title a')
            if self.test:
                detail_link_node_list = detail_link_node_list[:1]
            for detail_link_node in detail_link_node_list:
                detail_link = detail_link_node.attrib['href']
                yield Request(url=detail_link, callback=self.parse_detail, cb_kwargs=kwargs)
            next_link = response.css('a.aNxt').attrib.get('href')
            # 翻页
            if next_link is not None:
                yield Request(url=next_link, callback=self.parse, cb_kwargs=kwargs)
        elif info_type == 'zufang':
            detail_link_node_list = response.css('.zu-info h3 a')
            if self.test:
                detail_link_node_list = detail_link_node_list[:1]
            for detail_link_node in detail_link_node_list:
                detail_link = detail_link_node.attrib['href']
                yield Request(url=detail_link, callback=self.parse_detail, cb_kwargs=kwargs)
            next_link = response.css('a.aNxt').attrib.get('href')
            # 翻页
            if next_link is not None:
                yield Request(url=next_link, callback=self.parse, cb_kwargs=kwargs)


    def parse_detail(self, response, **kwargs):
        """
        解析detail页面的数据
        :param response:
        :param kwargs:
        :return:
        """
        info_type = kwargs.get('type')
        if info_type == 'ershoufang':
            item = ErShouFangSourceItem()
            item['city'] = self.city_map[kwargs.get('city')]
            item['area'] = kwargs.get('area', '')
            item['business_circle'] = kwargs.get('business_circle', '')
            item['village_name'] = response.css('.houseInfo-detail-list .houseInfo-content a:nth-child(1)::text').get(
                default='')
            item['listing_time'] = ''
            item['orientation'] = response.css(
                'div.houseInfo-wrap ul.houseInfo-detail-list li.houseInfo-detail-item:nth-child(8) > div.houseInfo-content::text').get(
                default='').strip()
            item['residence_room'] = response.css(
                'div.houseInfo-wrap ul.houseInfo-detail-list li.houseInfo-detail-item:nth-child(2) > div.houseInfo-content::text').get(
                default='').strip().replace('\t', '').replace('\n', '')
            item['floor'] = response.css(
                'div.houseInfo-wrap ul.houseInfo-detail-list li.houseInfo-detail-item:nth-child(11) > div.houseInfo-content::text').get(
                default='').strip()
            item['area1'] = response.css(
                'div.houseInfo-wrap ul.houseInfo-detail-list li.houseInfo-detail-item:nth-child(5) > div.houseInfo-content::text').get(
                default='').strip().replace('平方米', '')
            item['area2'] = ''
            item['all_price'] = response.css(
                'div.houseInfo-wrap ul.houseInfo-detail-list li.houseInfo-detail-item:nth-child(6) > div.houseInfo-content::text').get(
                default='').strip().replace('万', '')
            item['single_price'] = response.css(
                'div.houseInfo-wrap ul.houseInfo-detail-list li.houseInfo-detail-item:nth-child(3) > div.houseInfo-content::text').get(
                default='').replace('元/m²', '').strip()
            item['build_time'] = response.css(
                'div.houseInfo-wrap ul.houseInfo-detail-list li.houseInfo-detail-item:nth-child(7) > div.houseInfo-content::text').get(
                default='').strip()
            item['link'] = response.url
            yield item
        elif info_type == 'zufang':
            html_str = response.text
            bs64_str = re.findall("charset=utf-8;base64,(.*?)'\)", html_str)[0]
            item = RentingHouseSourceItem()
            item['city'] = kwargs.get('city')
            item['area'] = kwargs.get('area')
            item['business_circle'] = kwargs.get('business_circle', '')
            item['village_name'] = response.css('.house-info-item a:nth-child(2)::text').get(default='')
            item['residence_room'] =''.join(response.xpath("//ul[@class='house-info-zufang cf']//li[2]//span[2]//text()").getall())
            item['orientation'] = response.css('.house-info-item:nth-child(4) .info::text').get(default='')
            item['floor'] = response.css('.house-info-item:nth-child(5) .info::text').get(default='')
            item['house_area'] = response.xpath("//li[@class='house-info-item']//b[@class='strongbox']/text()").get(default='').replace('平方米', '')
            item['price'] = response.xpath("//span[@class='price']//b[@class='strongbox']/text()").get(default='')
            item['renting_time'] = response.css(
                'div.content__article__info:nth-child(2) > ul:nth-child(3) > li:nth-child(2)::text').get(
                default='').replace('租期：', '')
            item['link'] = response.url

            item['residence_room'] = decrypt_text(item['residence_room'], bs64_str)
            item['price'] = decrypt_text(item['price'], bs64_str)
            item['house_area'] = decrypt_text(item['house_area'], bs64_str)
            return item


    def parse_village_info(self, response, **kwargs):
        """
        分析小区信息
        :param response:
        :param kwargs:
        :return:
        """
        item = kwargs.get('item')
        item['avg_price'] = response.xpath("//span[@class='average']/text()").get(default='')
        try:
            item['xqspfd'] = round(100 * float(item['price']) / float(item['avg_price']), 2)
        except ValueError or ZeroDivisionError:
            item['xqspfd'] = ''
        return item