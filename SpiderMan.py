#!/usr/bin/env python3
# -*- coding=UTF-8 -*-

from SpiderTools.DataOutput import DataOutput
from SpiderTools.HtmlDownloader import HtmlDownloader
from SpiderTools.HtmlParser import HtmlParser
from SpiderTools.URLManager import UrlManager

class SpiderMan(object):
    def __init__(self):
        self.manager = UrlManager()
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        self.output = DataOutput()

    def crawl(self,root_url):
        self.manager.add_new_url(root_url)
        while(self.manager.has_new_url() and self.manager.old_url_size()<100):
            try:
                new_url = self.manager.get_new_url()
                html = self.downloader.download(new_url)
                new_urls,data= self.parser.parser(new_url,html)
                self.manager.add_new_urls(new_urls)
                self.output.store_data(data)
                print("aready crawled %s link" %self.manager.old_url_size())
            except Exception as e:
                print("cause %s,crawl failed"%e)
        self.output.output_html()


if __name__ == "__main__":
    spider_man = SpiderMan()
    spider_man.crawl("https://baike.baidu.com/item/%E4%BA%8C%E6%AC%A1%E5%85%83/85064")
