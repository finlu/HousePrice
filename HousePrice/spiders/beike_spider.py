# -*- coding: utf-8 -*-
import re
import json
import scrapy
from scrapy.http import Request, JsonRequest, Response
from HousePrice.items import ErShouFangCityItem, ErShouFangVillageItem, ErShouFangSourceItem, RentingHouseSourceItem, \
    NewHouseItem


class BeikeSpiderSpider(scrapy.Spider):
    name = 'beike_spider'
    allowed_domains = ['ke.com']

    def __init__(self):
        super(BeikeSpiderSpider, self).__init__()
        self.test = True
        self.city_area_info = {
            'bj': {
                'dongcheng': '东城区',
                'xicheng': '西城区',
                'chaoyang': '朝阳区',
                'haidian': '海淀区',
                'tongzhou': '通州区',
                'shunyi': '顺义区'
            },
            # 'gz': {
            #     'haizhu': '海珠区',
            #     'huangpugz': '黄埔区',
            #     'tianhe': '天河区',
            #     'panyu': '番禺区',
            #     'nansha': '南沙区',
            #     'yuexiu': '越秀区',
            #     'liwan': '荔湾区',
            #     'baiyun': '白云区',
            # },
            # 'sz': {
            #     'luohuqu': '罗湖区',
            #     'futianqu': '福田区',
            #     'nanshanqu': '南山区',
            #     'yantianqu': '盐田区',
            #     'baoanqu': '宝安区',
            #     'longgangqu': '龙岗区',
            #     'longhuaqu': '龙华区',
            #     'guangmingqu': '光明区',
            #     'pingshanqu': '坪山区',
            # }
        }
        self.zufang_city_area_info = {
            'gz': {
                'haizhu': '海珠区',
                'huangpugz': '黄埔区',
                # 'tianhe': '天河区',
                # 'panyu': '番禺区',
                # 'nansha': '南沙区',
                # 'yuexiu': '越秀区',
                # 'liwan': '荔湾区',
                # 'baiyun': '白云区',
            },
            # 'sz': {
            #     'luohuqu': '罗湖区',
            #     'futianqu': '福田区',
            #     'nanshanqu': '南山区',
            #     'yantianqu': '盐田区',
            #     'baoanqu': '宝安区',
            #     'longgangqu': '龙岗区',
            #     'longhuaqu': '龙华区',
            #     'guangmingqu': '光明区',
            #     'pingshanqu': '坪山区',
            # }
        }
        self.xinfang_city_area_info = {
            'gz': {
                'haizhu': {
                    'name': '海珠区',
                    't': ''
                },
                # 'huangpugz': {
                #     'name': '黄埔区',
                #     't': ''
                # },
                # 'tianhe': {
                #     'name': '天河区',
                #     't': ''
                # },
                # 'panyu': {
                #     'name': '番禺区',
                #     't': ''
                # },
                # 'nansha': {
                #     'name': '南沙区',
                #     't': ''
                # },
                # 'yuexiu': {
                #     'name': '越秀区',
                #     't': ''
                # },
                # 'liwan': {
                #     'name': '荔湾区',
                #     't': ''
                # },
                # 'baiyun': {
                #     'name': '白云区',
                #     't': ''
                # },
            },
            # 'sz': {
            #     'luohuqu': {
            #         'name': '罗湖区',
            #         't': ''
            #     },
            #     'futianqu': {
            #         'name': '福田区',
            #         't': ''
            #     },
            #     'nanshanqu': {
            #         'name': '南山区',
            #         't': ''
            #     },
            #     'yantianqu': {
            #         'name': '盐田区',
            #         't': ''
            #     },
            #     'baoanqu': {
            #         'name': '宝安区',
            #         't': ''
            #     },
            #     'longgangqu': {
            #         'name': '龙岗区',
            #         't': ''
            #     },
            #     'longhuaqu': {
            #         'name': '龙华区',
            #         't': ''
            #     },
            #     'guangmingqu': {
            #         'name': '光明区',
            #         't': ''
            #     },
            #     'pingshanqu': {
            #         'name': '坪山区',
            #         't': ''
            #     },
            # }
        }

    def start_requests(self):
        # 二手房
        for city, area_info in self.city_area_info.items():
            for area_code, area_name in self.city_area_info[city].items():
                url = 'https://{}.ke.com/ershoufang/{}/'.format(city, area_code)
                yield Request(url=url, callback=self.parse_index,
                              cb_kwargs={'city': city, 'area': area_name, 'area_code': area_code, 'type': 'ershoufang'},
                              dont_filter=True)
        # 租房
        for city, area_info in self.zufang_city_area_info.items():
            for area_code, area_name in self.zufang_city_area_info[city].items():
                url = 'https://{}.zu.ke.com/zufang/{}/'.format(city, area_code)
                yield Request(url=url, callback=self.parse_index,
                              cb_kwargs={'city': city, 'area': area_name, 'area_code': area_code, 'type': 'zufang'},
                              dont_filter=True)
        # 新房
        for city, area_info in self.xinfang_city_area_info.items():
            for area_code, area_name in self.xinfang_city_area_info[city].items():
                url = 'https://{}.fang.ke.com/loupan/{}/'.format(city, area_code)
                # 访问首页，获取之后所有的页面（翻页）
                yield Request(url=url, callback=self.parse_xinfang_index,
                              cb_kwargs={'city': city, 'area': area_name['name'], 'area_code': area_code,
                                         'type': 'xinfang'},
                              dont_filter=True, method='GET')

    def parse_xinfang_index(self, response, **kwargs):
        page_links = response.css('body:nth-child(2) > section.se-part:nth-child(11) a')
        for page_link in page_links:
            url = page_link.attrib['href'] + '?_t=1'
            yield Request(url=url, callback=self.parse_xinfang_list_page, cb_kwargs=kwargs)

    def parse_xinfang_list_page(self, response, **kwargs):
        data_list = json.loads(response.body)['data']['list']
        for data in data_list:
            item = NewHouseItem()
            item['city'] = kwargs.get('city')
            item['area'] = kwargs.get('area')
            item['name'] = data['resblock_name']
            item['another_name'] = data['resblock_alias']
            item['new_kp_time'] = data['open_date']
            item['new_kp_single_price'] = float(data['show_price'])
            item['new_kp_all_price'] = float(data['lowest_total_price']) / 10000
            item['link'] = 'https://{}.fang.ke.com/loupan/p_'.format(kwargs.get('city')) + data['project_name'] + '/'
            yield item

    def parse_village_trend(self, response: Response, **kwargs):
        url = re.search(r"analysis.init\('(.*?)'\)", response.text).group(1)
        yield Request(url='https://bj.ke.com' + url, callback=self.yield_city_item, cb_kwargs=kwargs)

    def yield_city_item(self, response, **kwargs):
        item = kwargs.get('city_item')
        total_price = json.loads(response.text)['currentLevel']['listPrice']['total']
        item['avg_price'] = total_price[0]
        item['price_width'] = round(100 * (total_price[0] - total_price[-1]) / total_price[-1], 2)
        return item

    def parse_index(self, response, **kwargs):
        info_type = kwargs.get('type')
        city_name = kwargs.get('city')
        if info_type == 'ershoufang':
            guapan_num = response.css('h2.total span::text').get(default='').strip()  # 区的挂盘数量
            item = ErShouFangCityItem()
            item['city'] = city_name
            item['area'] = kwargs.get('area')
            item['guapan_num'] = guapan_num
            yield Request('https://{}.ke.com/fangjia/{}/'.format(kwargs['city'], kwargs['area_code']),
                          callback=self.parse_village_trend, cb_kwargs={'city_item': item})
            bankuai_list = response.css(
                'div.position dl:nth-child(2) dd:nth-child(2) div:nth-child(1) > div:nth-child(2) > a')
            for bankuai in bankuai_list:
                # 翻页
                page_info = json.loads(response.css('.page-box::attr(page-data)').get())
                for page in range(page_info['totalPage'])[:1]:
                    bankuai_name = bankuai.css('::text').get(default='')
                    kwargs.update({'bankuai_name': bankuai_name})
                    url = 'https://{}.ke.com'.format(city_name) + bankuai.attrib['href'] + 'pg{}sf1/'.format(page + 1)
                    yield Request(url=url, callback=self.parse_list_page, cb_kwargs=kwargs)
        elif info_type == 'zufang':
            # 去除第一个不限的链接
            bankuai_list = response.css(
                '#filter > ul:nth-child(4) a')[1:]
            if self.test:
                bankuai_list = bankuai_list[:1]
            for bankuai in bankuai_list:
                # 翻页
                total_page = int(response.css('.content__pg::attr(data-totalpage)').get())
                page_range = range(total_page)
                if self.test:
                    page_range = page_range[:1]
                for page in page_range:
                    bankuai_name = bankuai.css('::text').get(default='')
                    kwargs.update({'bankuai_name': bankuai_name})
                    url = 'https://{}.zu.ke.com'.format(city_name) + bankuai.attrib['href'] + 'pg{}/'.format(page + 1)
                    yield Request(url=url, callback=self.parse_list_page, cb_kwargs=kwargs)

    def parse_village_info(self, response, **kwargs):
        item = kwargs.get('item')
        if isinstance(item, ErShouFangVillageItem):
            item['guapan_num'] = response.css('')
        item['village_avg_price'] = response.css('.xiaoquUnitPrice::text').get(default='')
        item['village_link'] = kwargs.get('village_url')
        return item

    def parse_list_page(self, response, **kwargs):
        info_type = kwargs.get('type')
        if info_type == 'ershoufang':
            # 板块的挂盘数量
            # guapan_num = response.css('h2.total span::text').get(default='').strip()
            node_list = response.css('#beike .sellListContent li.clear')
            for i, node in enumerate(node_list[:1]):
                item = ErShouFangVillageItem()
                item['city'] = kwargs.get('city')
                item['area'] = kwargs.get('area')
                item['bankuai_name'] = kwargs.get('bankuai_name')
                item['name'] = response.css('.positionInfo a::text').get(default='')
                # item['guapan_num'] = guapan_num
                village_url = response.css('.positionInfo a').attrib['href']
                yield Request(village_url, self.parse_village_info, cb_kwargs={'item': item, 'village_url': village_url}, dont_filter=True)
                # 获取当前页面所有房的链接
                url = node.css('.title a').attrib['href']
                self.logger.info(url)
                kwargs.update({
                    'village_url': village_url
                })
                yield Request(url=url, callback=self.parse_detail_item,
                              cb_kwargs=kwargs)
        elif info_type == 'zufang':
            node_list = response.css('.content__list--item .content__list--item--main')
            city_name = kwargs.get('city')
            for i, node in enumerate(node_list[:1]):
                try:
                    # 获取当前页面所有房的链接
                    url = 'https://{}.zu.ke.com'.format(city_name) + \
                          node.css('p.content__list--item--title.twoline a').attrib['href']
                    self.logger.info(url)
                    yield Request(url=url, callback=self.parse_detail_item,
                                  cb_kwargs=kwargs)
                except Exception as e:
                    # 遇到广告页面
                    pass

    def parse_detail_item(self, response, **kwargs):
        info_type = kwargs.get('type')
        if info_type == 'ershoufang':
            item = ErShouFangSourceItem()
            item['city'] = kwargs.get('city')
            item['area'] = kwargs.get('area')
            item['business_circle'] = kwargs.get('bankuai_name')
            item['village_name'] = response.css('.communityName a.info::text').get(default='')

            lis = response.css('.base .content ul li')
            for li in lis:
                span_text = li.css('span::text').get(default='')
                if span_text == '房屋户型':
                    item['residence_room'] = li.css('::text').getall()[1]
                elif span_text == '所在楼层':
                    item['floor'] = li.css('::text').getall()[1]
                elif span_text == '建筑面积':
                    item['area1'] = li.css('::text').getall()[1].replace('㎡', '')
                elif span_text == '套内面积':
                    item['area2'] = li.css('::text').getall()[1].replace('㎡', '')
                elif span_text == '房屋朝向':
                    item['orientation'] = li.css('::text').getall()[1]
                elif span_text == '挂牌时间':
                    item['listing_time'] = li.css('::text').getall()[1].replace('\n', '')
            check_field_list = ['residence_room', 'area1', 'area2', 'floor', 'orientation', 'listing_time']
            for check_field in check_field_list:
                if check_field not in item.keys():
                    item[check_field] = ''
            all_price = float(response.css('.price .total::text').get(default=0))
            single_price = float(response.css('.price .unitPriceValue::text').get(default=0))
            item['all_price'] = all_price
            item['single_price'] = single_price
            item['build_time'] = response.css('.area .subInfo::text').get(default='')
            item['link'] = response.url
            yield Request(url=kwargs.get('village_url'), callback=self.parse_village_info, cb_kwargs={'item': item, 'village_url': kwargs.get('village_url')}, dont_filter=True)
        elif info_type == 'zufang':
            item = RentingHouseSourceItem()
            item['city'] = kwargs.get('city')
            item['area'] = kwargs.get('area')
            item['business_circle'] = kwargs.get('bankuai_name')
            item['village_name'], item['residence_room'], item['orientation'] = response.css(
                '.content__title::text').get(default='').split(' ')
            # item['orientation'] = response.css('div.content__article__info:nth-child(2) > ul:nth-child(2) > li:nth-child(3)::text').get(default='').replace('朝向：', '')
            item['floor'] = response.css(
                'div.content__article__info:nth-child(2) > ul:nth-child(2) > li:nth-child(8)::text').get(
                default='').replace('楼层：', '')
            item['house_area'] = response.css(
                'div.content__article__info:nth-child(2) > ul:nth-child(2) > li:nth-child(2)::text').get(
                default='').replace('面积：', '').replace('㎡', '')

            item['price'] = response.css('div.content__aside--title span::text').get(default='')
            item['renting_time'] = response.css(
                'div.content__article__info:nth-child(2) > ul:nth-child(3) > li:nth-child(2)::text').get(
                default='').replace('租期：', '')
            item['link'] = response.url
            yield item
