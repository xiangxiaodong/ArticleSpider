# -*- coding: utf-8 -*-
import scrapy
import re
import json
from urllib import parse

class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    # mac端的chrome用户代理
    agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'
    
    header = {
        'HOST': 'www.zhihu.com',
        'Referer': 'https://www.zhihu.com',
        'User-Agent': agent
    }
    
    def parse(self, response):
        """
        提取出html页面中的所有url，并跟踪这些url进行爬取
        
        :param response:
        :return:
        """
        all_urls = response.xpath('')
        all_urls = [parse.urljoin(response.url,url) for url in all_urls]
        all_urls = filter(lambda x:True if x.startswith('https') else False,all_urls)
        for url in all_urls:
            pass
    
    def parse_detail(self,response):
        pass
    
    
    # 重写入口函数
    def start_requests(self):
        # 获取首页的_xsrf的code
        # 回调login函数
        return [scrapy.Request('https://www.zhihu.com/signin', headers=self.header, callback=self.login)]
    
    def login(self, response):
        # post_url = 'https://www.zhihu.com/'
        # response_text = response.text
        post_data = {
            '_xsrf': '704c97e7-a896-4df3-82c4-2c6bccda1612',
            'username': '17682310408',
            'password': 'xxd102401'
        }
        return [scrapy.FormRequest(  # formrequset函数可以完成表单的提交
            url='https://www.zhihu.com/signin',
            formdata=post_data,
            headers=self.header,
            callback=self.check_login,  # 回调验证函数
        )]
    
    def check_login(self, resqonse):
        #验证服务器的返回数据是否成功
        text_json = json.loads(resqonse.text)
        if 'msg' in text_json and text_json['msg'] == '登录成功':
            for url in self.start_urls:
                yield scrapy.Request(url,dont_filter=True,headers=self.header)
            