# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
import scrapy
import os
from scrapy.utils.project import get_project_settings

class DouyuPipeline(object):
    def process_item(self, item, spider):
        return item


class ImagePipeline(ImagesPipeline):
    IMAGES_STORE = get_project_settings().get('IMAGES_STORE')

    def get_media_requests(self, item, info):
        # 将需要下载的图片url做成请求返回给引擎,图片将会自动下载,请求不需要指定callback
        yield scrapy.Request(item['image_link'])

    def item_completed(self, results, item, info):
        # print(results)
        image_path = [data['path'] for ok, data in results if ok]
        print(image_path)
        # 构建旧文件名和新文件名
        old_path = self.IMAGES_STORE + os.sep + image_path[0]
        new_path = self.IMAGES_STORE + os.sep + image_path[0].split(os.sep)[0] + os.sep + item['nickname'] + '.jpg'
        # 重命名
        os.rename(old_path,new_path)
        item['image_path'] = new_path
        return item









