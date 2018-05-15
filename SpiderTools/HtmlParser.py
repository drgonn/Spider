#!/usr/bin/env python3
# -*- coding=UTF-8 -*-


import re,json
import urllib.parse
from bs4 import BeautifulSoup

class HtmlParser(object):
    def parser(self,page_url,html_cont):
        #param  下载的url和内容
        if page_url is None or html_cont is None:
            return
        soup = BeautifulSoup(html_cont,'html.parser')
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

    #爬取电影
    def parser_url(self,page_url,response):
        pattern = re.compile(r'http://movie.mtime.com/(\d+)/')
        urls = pattern.findall(response)
        if urls != None:
            return list(set(urls))
        else:
            return None

    def parser_json(selfself,page_url,response):
        pattern = re.compile(r'=(.*?);')
        result = pattern.findall(resopnse)[0]
        if result!=None:
            value=json.loads(result)
            try:
                isRelease = value.get('value').get('isRelease')
            except Exception as e:
                print(e)
                return None
            if isRelease:
                if value.get('value').get('hotValue')==None:
                    return self._parser_release(page_url,value)
                else:
                    return self._parser_no_release(page_url,value,isRelease=2)
            else:
                return self._parser_release(page_url,value)

    def _parser_release(selfself,page_url,value):
        try:
            isRelease = 1
            movieRating = value.get('value').get('movieRating')
            boxOffice = value.get('value').get('boxOffice')
            movieTitle = value.get('value').get('movieTitle')
            RPictureFinal=movieRating.get('RPictureFinal')
            RStoryFinal = movieRating.get('RStoryFinal')
            RDirectorFinal = movieRating.get('RDirectorFinal')
            ROtherFinal = movieRating.get('ROtherFinal')
            RatingFinal = movieRating.get('RatingFinal')

















