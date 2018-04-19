# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from urllib import parse
<<<<<<< HEAD
from ArticleSpider.utils.common import get_md5
from ArticleSpider.items import JobBoleArticleItem,ArticleItemLoader
import datetime
from scrapy.loader import ItemLoader
=======

# from ArticleSpider.items import JoBoleArticleItem

>>>>>>> master

class JobbleSpider(scrapy.Spider):
    name = 'jobble'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']
    
    def parse(self, response):
        # 解析列表页面中的所有文章url并且交给scrapy下载后并进行解析
        post_nodes = response.xpath('//div[@id="archive"]/div[@class="post floated-thumb"]/div[@class="post-thumb"]/a')
        for post_node in post_nodes:
            image_url = post_node.xpath('./img/@src').extract_first()
            post_url = post_node.xpath('./@href').extract_first()
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": image_url},
                          callback=self.parse_detail)
        
        # 提取下一页，交给scrapy下载
        next_urls = response.xpath('//a[@class="next page-numbers"]/@href').extract_first()
        if next_urls:
            yield Request(url=parse.urljoin(response.url, next_urls), callback=self.parse)
    
    def parse_detail(self, response):
<<<<<<< HEAD
        # article_item = JobBoleArticleItem()
        front_image_url = response.meta.get('front_image_url', '')  # 文章封面图的url
        # # 提取文章的具体字段
        # title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first()
        # create_date = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract_first().strip().replace(
        #     '·', '').strip()
        # praise_nums = response.xpath("//span[contains(@class,'vote-post-up')]/h10/text()").extract_first()
        # fav_nums = response.xpath("//span[contains(@class,'bookmark-btn')]/text()").extract_first()
        # match_re = re.match(".*?(\d+).*", fav_nums)
        # if match_re:
        #     fav_nums = int(match_re.group(1))
        # else:
        #     fav_nums = 0
        # comment_nums = response.xpath("//a[@href='#article-comment']/text()").extract_first()
        # match_re = re.match(".*?(\d+).*", comment_nums)
        # if match_re:
        #     comment_nums = int(match_re.group(1))
        # else:
        #     comment_nums = 0
        # content = response.xpath("//div[@class='entry']/p/text()").extract()
        # content = ''.join(content)
        #
        # tag_list = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
        # tag_list = [tag for tag in tag_list if not tag.strip().endswith('评论')]
        # tags = ','.join(tag_list)
        # article_item['url_object_id'] = get_md5(response.url)
        # article_item["title"] = title
        # article_item["url"] = response.url
        # try:
        #     create_date = datetime.datetime.strptime(create_date,'%Y/%m/%d').date()
        # except Exception as e:
        #     create_date = datetime.datetime.now().date()
        # article_item["create_date"] = create_date
        # article_item["front_image_url"] = [front_image_url]
        # article_item["praise_nums"] = praise_nums
        # article_item["tags"] = tags
        # article_item["fav_nums"] = fav_nums
        # article_item["content"] = content
        
        #通过Itenmloader加载item
        item_loader = ArticleItemLoader(item=JobBoleArticleItem(),response=response)#实例化（具体化哪个需要loader）
        item_loader.add_xpath('title','//div[@class="entry-header"]/h1/text()')
        item_loader.add_xpath('create_date','//p[@class="entry-meta-hide-on-mobile"]/text()')
        item_loader.add_value('url',response.url)#直接传值给url
        item_loader.add_value('url_object_id',get_md5(response.url))
        item_loader.add_value('front_image_url',[front_image_url])
        item_loader.add_xpath('comment_nums',"//a[@href='#article-comment']/text()")
        item_loader.add_xpath('fav_nums',"//span[contains(@class,'bookmark-btn')]/text()")
        item_loader.add_xpath('tags',"//p[@class='entry-meta-hide-on-mobile']/a/text()")
        item_loader.add_xpath('content',"//div[@class='entry']/p/text()")
        
        article_item = item_loader.load_item()#解析到item中去
        
        
        yield article_item
=======
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
        
>>>>>>> master
