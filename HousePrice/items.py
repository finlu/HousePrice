import scrapy


class ErShouFangCityItem(scrapy.Item):
    city = scrapy.Field()  # 城市
    area = scrapy.Field()  # 所属区
    guapan_num = scrapy.Field()  # 挂盘数量
    avg_price = scrapy.Field()  # 均价（=本版块所有在售房源价格的平均价）
    price_width = scrapy.Field()  # 价格增幅（=本月均价/上月均价*100%）


class ErShouFangVillageItem(scrapy.Item):
    city = scrapy.Field()  # 城市
    area = scrapy.Field()  # 小区所属区
    bankuai_name = scrapy.Field()  # 板块
    name = scrapy.Field()  # 小区名称
    guapan_num = scrapy.Field()  # 挂盘数量
    village_avg_price = scrapy.Field()  # 小区均价（元）
    village_link = scrapy.Field()  # 小区链接


class ErShouFangSourceItem(scrapy.Item):
    city = scrapy.Field()  # 城市
    area = scrapy.Field()  # 城区
    business_circle = scrapy.Field()  # 商圈
    village_name = scrapy.Field()  # 小区名
    listing_time = scrapy.Field()  # 挂牌时间
    orientation = scrapy.Field()  # 朝向
    residence_room = scrapy.Field()  # 房屋户型
    floor = scrapy.Field()  # 楼层
    area1 = scrapy.Field()  # 建筑面积
    area2 = scrapy.Field()  # 套内面积
    all_price = scrapy.Field()  # 总价 （万元）
    single_price = scrapy.Field()  # 单价 （元）
    village_avg_price = scrapy.Field()  # 小区均价 （元）
    village_link = scrapy.Field()  # 小区链接
    xqspfd = scrapy.Field()  # 小区笋盘幅度
    build_time = scrapy.Field()  # 建筑时间
    link = scrapy.Field()  # 房源链接


class RentingHouseSourceItem(scrapy.Item):
    city = scrapy.Field()  # 城市
    area = scrapy.Field()  # 城区
    business_circle = scrapy.Field()  # 商圈
    village_name = scrapy.Field()  # 小区名
    orientation = scrapy.Field()  # 朝向
    residence_room = scrapy.Field()  # 居/室
    office = scrapy.Field()  # 厅
    floor = scrapy.Field()  # 楼层
    house_area = scrapy.Field()  # 面积
    price = scrapy.Field()  # 租价
    renting_time = scrapy.Field()  # 租期
    link = scrapy.Field()  # 租房房源链接


class NewHouseItem(scrapy.Item):
    city = scrapy.Field()  # 城市
    area = scrapy.Field()  # 新盘所属区
    name = scrapy.Field()  # 新盘名称
    another_name = scrapy.Field()  # 别名
    new_kp_time = scrapy.Field()  # 最新开盘时间
    new_kp_single_price = scrapy.Field()  # 新盘单价（元）（均价）
    new_kp_all_price = scrapy.Field()  # 新盘总价（万元）（均价）
    link = scrapy.Field()  # 新盘链接
