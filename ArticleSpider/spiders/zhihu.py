# -*- coding: utf-8 -*-
import scrapy
import re
import json
from urllib import parse
from scrapy.loader import ItemLoader
from items import ZhihuQuestionItem,ZhihuAnswerItem

class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    # mac端的chrome用户代理
    # agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'
    # win10
    # agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'
    header = {
        'HOST': 'www.zhihu.com',
        'Referer': 'https://www.zhihu.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'
    }
    
    def parse(self, response):
        """
        提取出html页面中的所有url，并跟踪这些url进行爬取
        
        :param response:
        :return:
        """
        all_urls = response.css("a::attr(href)").extract()
        all_urls = [parse.urljoin(response.url, url) for url in all_urls]
        all_urls = filter(lambda x: True if x.startswith('https') else False, all_urls)  # 过滤非url
        for url in all_urls:
            print(url)
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", url)
            if match_obj:
                request_url = match_obj.group(1)
                question_id = match_obj.group(2)
                yield scrapy.Request(request_url, headers=self.header, callback=self.parse_question)
    
    def parse_question(self, response):
        # 处理question页面，从页面中提取出具体的question item
        if 'QuestionHeader-title' in response.text:
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*",response.url)
            if match_obj:
                question_id = int(match_obj.group(2))
            # 处理新版本,使用loader方法
            item_loader = ItemLoader(item=ZhihuQuestionItem(),response=response)
            item_loader.add_xpath('title','//h1[@class="QuestionHeader-title"]/text()')
            item_loader.add_xpath('content','//span[@class="RichText"]/text()')
            item_loader.add_value('url',response.url)
            item_loader.add_value('zhihu_id',question_id)
            item_loader.add_css('answer_num','')
            item_loader.add_xpath('contents_num','//button[@class="Button Button--plain Button--withIcon Button--withLabel"]/text()')
            item_loader.add_xpath('watch_user_num','//strong[@class="NumberBoard-itemValue"]/text()')
            item_loader.add_xpath('topics','//div[@class="Popover"]/div/text()')
            
            question_item = item_loader.load_item()
        else:
            #处理老版本页面的item提取
            pass
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
            '_xsrf': '72c8bb65-c5e4-48ea-b95b-99bf4cd0dc14',
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
        # 验证服务器的返回数据是否成功
        text_json = json.loads(resqonse.text)
        if 'msg' in text_json and text_json['msg'] == '登录成功':
            for url in self.start_urls:
                yield scrapy.Request(url, dont_filter=True, headers=self.header)
