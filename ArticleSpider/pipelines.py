# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
import codecs
import json
from scrapy.exporters import JsonItemExporter
import MySQLdb


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item


# 将item的数据以json文件保存的pipelines
class JsonWithEncodeingPipeline(object):
    # 自定义json文件的导出
    def __init__(self):  # 打开json文件
        self.file = codecs.open('article.json', 'w', encoding='utf-8')
    
    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(lines)
        return item  # 返回item
    
    def spider_closed(self, spider):  # 关闭json文件
        self.file.close()


class JsonExportPipeline(object):
    # 调用scrapy提供的json export导出json文件
    def __init__(self):  # 初始化
        self.file = open('articleexport.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()
    
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
    
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


# 处理图片的路径
class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok, value in results:
            image_file_path = value['path']
        item['front_image_path'] = image_file_path
        
        return item


# 保存到mysql数据库
class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(
            'localhost',
            'root',
            'root',
            'article',
            charset='utf8',
            use_unicode=True,
        )
        self.cursor = self.conn.cursor()
    
    def process_item(self, item, spider):
        insert_sql = """
        insert into jobbole_article(title,url,create_date,fav_nums)
        VALUES (%s,%s,%s,%s)
        """
        self.cursor.execute(insert_sql,
                            (item['title'], item['url'],
                             item['create_date'],item['fav_nums'])
                            )
        self.conn.commit()
