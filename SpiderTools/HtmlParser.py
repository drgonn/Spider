#!/usr/bin/env python3
# -*- coding=UTF-8 -*-


import re
import urllib.parse
from bs4 import BeautifulSoup

class HtmlParser(object):
    def parser(self,page_url,html_cont):
        #param  下载的url和内容
        if page_url is None or html_cont is None:
            return
        soup = BeautifulSoup(html_cont,'html.parse',from_encoding='utf-8')
        new_urls = self._get_new_urls(page_url,soup)
        new_data = self._get_new_data(page_url,soup)
        return new_urls,new_data

    def _get_new_urls(self,page_url,soup):
        new_urls = set()
        links = soup.find_all('a',href= re.compile(r'/item/%'))
        for link in links:
            new_url=link['href']
            new_ful_url = urllib.parse.urljoin(page_url,new_url)
            new_urls.add(new_ful_url)
        return new_urls

    def _get_new_data(self,page_url,soup):
        data = {}
        data['url'] = page_url
        title = soup.find('dd',class_='lemmaWgt-lemmaTitle-title').find('h1')
        data['title']=title.get_text()
        summary=soup.find('div',class_='lemma-summary')
        data['summary'] = summary.get_text()
        return data










