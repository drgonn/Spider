#!/usr/bin/env python3
# -*- coding=UTF-8 -*-


from SpiderTools.HtmlDownloader import HtmlDownloader
from SpiderTools.HtmlParser import HtmlParser
from multiprocessing.managers import BaseManager
from multiprocessing import Process
import random,time
from queue import Queue

class QueueManager(BaseManager):
    pass



class SpiderChild(object):
    def __init__(self):
        QueueManager.register('get_task_queue')
        QueueManager.register('get_result_queue')
        server_addr='127.0.0.1'
        print('Connect to server %s ...' %server_addr)
        self.m=QueueManager(address=(server_addr,8001),
                            authkey='qiye'.encode('utf-8'))
        self.m.connect()
        self.task = self.m.get_task_queue()
        self.result = self.m.get_result_queue()
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser
        print('Init finished')


    def crawl(self):
        while (True):
            try:
                print(self.task.empty())
                time.sleep(1)
                if not self.task.empty():
                    print(self.task.empty())
                    print("OKOKOKOKOKOKOK")
                    url = self.task.get(True)
                    if url == 'end':
                        print('控制节点通知爬虫节点停止工作。')
                        self.result.put({'new_urls':'end','data':'end'})
                        return
                    print('爬虫节点正在解析：%s'%url)
                    content = self.downloader.download(url)
                    new_urls,data = self.parser.parser(url,content)
                    self.result.put({"new_urls":new_urls,"data":data})
            except EOFError as e:
                print("连接工作节点失败")
                return
            except Exception as e:
                print(e)
                print("爬取失败")





if __name__ == "__main__":
    spider = SpiderChild()
    spider.crawl()