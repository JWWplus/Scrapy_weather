# -*- coding: utf-8 -*-
import scrapy
from weather.items import WeatherItem
import sys

reload(sys)

sys.setdefaultencoding('utf-8')


class WeatherSpider(scrapy.Spider):
    # name属性是区别各个爬虫类的唯一标志
    name = "myweather"
    allowed_domains = ["sina.com.cn"]
    # 抓取的起始位置
    start_urls = ['http://weather.sina.com.cn']

    def parse(self, response):
        # 首先实例化item对象
        item = WeatherItem()
        # 前面两个利用xpath语法提取
        item['city'] = response.xpath('//*[@id="slider_ct_name"]/text()').extract()
        tenDay = response.xpath('//*[@id="blk_fc_c0_scroll"]')
        # 利用css选择器进行二次提取
        # p标签下class为wt_fc_c0_i_date的提取这个的文本
        item['date'] = tenDay.css('p.wt_fc_c0_i_date::text').extract()
        # 提取的是标题
        item['dayDesc'] = tenDay.css('img.icons0_wt::attr(title)').extract()
        item['dayTemp'] = tenDay.css('p.wt_fc_c0_i_temp::text').extract()
        return item
        # xpath(): 传入xpath表达式，返回该表达式所对应的所有节点的selector list列表 。
        # css(): 传入CSS表达式，返回该表达式所对应的所有节点的selector list列表.
        # extract(): 序列化该节点为unicode字符串并返回list。
        # re(): 根据传入的正则表达式对数据进行提取，返回unicode字符串list列表