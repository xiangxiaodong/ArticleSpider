# -*- coding: utf-8 -*-
import scrapy
import re


class JobbleSpider(scrapy.Spider):
    name = 'jobble'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/110287/']
    
    def parse(self, response):
        post_urls = response.xpath(
            '//div[@id="archive"]/div[@class="post floated-thumb"]/div[@class="post-thumb"]/a/@href').extract()
        title = response.xpath('//*[@id="post-110287"]/div[1]/h1/text()').extract_first()
        create_date = response.xpath('//*[@id="post-110287"]/div[2]/p/text()').extract_first().strip().strip(
            '·').strip()
        praise_num = response.xpath("//span[contains(@class,'vote-post-up')]/h10/text()").extract_first()
        fav_nums = response.xpath("//span[contains(@class,'bookmark-btn')]/text()").extract_first()
        match_re = re.match(".*?(\d+).*", fav_nums)
        if match_re:
            fav_nums = match_re.group(1)
        comment_nums = response.xpath("//a[@href='#article-comment']/text()").extract_first()
        match_re = re.match(".*?(\d+).*", comment_nums)
        if match_re:
            comment_nums = match_re.group(1)
        content = response.xpath("//div[@class='entry']").extract_first()
        
        tag_list = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
        tag_list = [tag for tag in tag_list if not tag.strip().endswith('评论')]
        tag_list = '，'.join(tag_list)
        pass
