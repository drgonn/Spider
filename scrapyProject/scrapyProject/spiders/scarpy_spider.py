#!/usr/bin/env python3
# coding:utf-8


from ..items import ScrapyprojectItem
import scrapy
from scrapy.selector import Selector
import urllib.parse
import time as sleep

class CnblgsSpider(scrapy.Spider):
	name="cnblogs"
	allowed_domains = ["biketo.com","bbs.biketo.com"]
	start_urls = ["http://bbs.biketo.com/index.html"]

	def  parse(self,response):
		
		papers = response.xpath(".//ul[@id='news']/li")

		for paper in papers:
			new_url=paper.xpath(".//div[@class='listl']/a/@href").extract()[0]
			url = urllib.parse.urljoin(self.start_urls[0],new_url)
			title = paper.xpath(".//div[@class='listr']/h3/a/text()").extract()[0]
			time = paper.xpath(".//em[@class='date']/text()").extract()[0]
			try:
				content = paper.xpath(".//div[@class='thread_summary']/text()").extract()[0]
			except IndexError:
				content = ""
			item = ScrapyprojectItem(url=url,title=title,time=time,content=content)
			request = scrapy.Request(url=url,callback=self.parse_body)
			
			# yield item



			request = scrapy.Request(url=url,callback=self.parse_body)
			# print("@"*100)
			request.meta['item'] = item
			yield request
		next_p = Selector(response).re('<a href="(\S*)"\sclass="nxt">下一页</a>')
		if next_p:
			next_page=urllib.parse.urljoin(self.start_urls[0],next_p[0])
			yield scrapy.Request(url=next_page,callback=self.parse)

	def parse_body(self,response):
		item = response.meta['item']
		body = response.xpath(".//*[@class='mn']")
		# item['image_urls'] =[urllib.parse.urljoin(self.start_urls[0],url) for url in body.xpath('.//img//@src').extract()]
		item['image_urls'] = body.xpath('.//img[@class="zoom"]/@file').extract()

		yield item





