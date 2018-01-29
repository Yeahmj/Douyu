# -*- coding: utf-8 -*-
import scrapy
import json

from Douyu.items import DouyuItem


class DouyuSpider(scrapy.Spider):
    name = 'douyu'
    allowed_domains = ['douyucdn.cn']
    base_url = 'http://capi.douyucdn.cn/api/v1/getVerticalRoom?limit=100&offset='
    # 网址limit=100参数设默认参数为0
    offset = 0
    start_urls = [base_url]

    def parse(self, response):
        # 获取房间节点列表  json.loads转换为字典格式
        node_list = json.loads(response.body.decode())['data']

        # 遍历房间节点列表
        for node in node_list:
            item = DouyuItem()
            item['nickname'] = node['nickname']
            item['uid'] = node['owner_uid']
            item['image_link'] = node['vertical_src']
            item['city'] = node['anchor_city']

            yield item

        # 模拟翻页
        if len(node_list) == 100:
            self.offset += 100
            # 拼接url
            next_url = self.base_url + str(self.offset)
            yield scrapy.Request(next_url,callback=self.parse)


