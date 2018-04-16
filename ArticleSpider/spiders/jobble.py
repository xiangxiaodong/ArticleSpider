# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from urllib import parse

# from ArticleSpider.items import JoBoleArticleItem


class JobbleSpider(scrapy.Spider):
    name = 'jobble'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']
    
    def parse(self, response):
        # 解析列表页面中的所有文章url并且交给scrapy下载后并进行解析
        post_urls = response.xpath('//div[@id="archive"]/div[@class="post floated-thumb"]/div[@class="post-thumb"]/a/@href').extract()
        for post_url in post_urls:
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse_detail)
        
        # 提取下一页，交给scrapy下载
        next_urls = response.xpath('//a[@class="next page-numbers"]/@href').extract_first()
        if next_urls:
            yield Request(url=parse.urljoin(response.url, next_urls), callback=self.parse)
    
    def parse_detail(self, response):
        # article_item = JoBoleArticleItem()
        # 提取文章的具体字段
        title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first()
        create_date = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract_first().strip().replace(
            '·', '').strip()
        praise_nums = response.xpath("//span[contains(@class,'vote-post-up')]/h10/text()").extract_first()
        fav_nums = response.xpath("//span[contains(@class,'bookmark-btn')]/text()").extract_first()
        match_re = re.match(".*?(\d+).*", fav_nums)
        if match_re:
            fav_nums = int(match_re.group(1))
        else:
            fav_nums = 0
        comment_nums = response.xpath("//a[@href='#article-comment']/text()").extract_first()
        match_re = re.match(".*?(\d+).*", comment_nums)
        if match_re:
            comment_nums = int(match_re.group(1))
        else:
            comment_nums = 0
        content = response.xpath("//div[@class='entry']").extract_first()
        
        tag_list = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
        tag_list = [tag for tag in tag_list if not tag.strip().endswith('评论')]
        tags = ','.join(tag_list)
        # article_item["title"] = title
        # article_item["url"] = response.url
        