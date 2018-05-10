#!/usr/bin/env python3
# -*- coding=UTF-8 -*-

from SpiderTools.DataOutput import DataOutput
from SpiderTools.HtmlDownloader import HtmlDownloader
from SpiderTools.HtmlParser import HtmlParser
from SpiderTools.URLManager import UrlManager
from multiprocessing.managers import BaseManager
from multiprocessing import Process
import random,time
from queue import Queue

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

class QueueManager(BaseManager):
    pass

class NodeManager(object):
    def start_Manager(self,url_q,result_q):
        #创建分布式管理器
        QueueManager.register('get_task_queue',callable=lambda:url_q)
        QueueManager.register('get_result_queue',callable = lambda:result_q)
        manager = QueueManager(address=('',8001),authkey='qiye'.encode('utf-8'))
        return manager

    def url_manager_proc(self,url_q,conn_q,root_url):
        url_manager = UrlManager()
        url_manager.add_new_url(root_url)
        while True:
            while(url_manager.has_new_url()):
                new_url = url_manager.get_new_url()
                url_q.put(new_url)
                print('old_url=',url_manager.old_url_size())#
                if (url_manager.old_url_size()>20):
                    url_q.put('end')
                    print("控制节点爬满2000结束！")
                    url_manager.save_progress('new_urls.txt',url_manager.new_urls)
                    return
            try:
                if not conn_q.empty():
                    urls = conn_q.get()
                    url_manager.add_new_urls(urls)
            except BaseException as e:
                time.sleep(0.1)

    def result_solve_proc(self,result_q,conn_q,store_q):
        while(True):
            try:
                if not result_q.empty():
                    content = result_q.get(True)
                    if content['new_urls']=='end':
                        print("爬完了！")
                        store_q.put('end')
                        return
                    conn_q.put(content['new_urls'])# put的set类型
                    store_q.put(content['data'])# 发送的是dict类型
                else:
                    time.sleep(0.1)
            except BaseException as e:
                time.sleep(0.1)

    def store_proc(self,store_q):
        output = DataOutput()
        while True:
            if not store_q.empty():
                data = store_q.get()
                if data == 'end':
                    print("存储进程接受通知然后结束")
                    output.output_end(output.filepath)
                    return
                output.store_data(data)
            else:
                time.sleep(0.1)

root_url = "https://baike.baidu.com/item/%E9%AB%98%E6%BD%AE/5604214?fr=aladdin"

if __name__ == "__main__":
    url_q = Queue()
    result_q = Queue()
    store_q = Queue()
    conn_q = Queue()
    node = NodeManager()
    manager = node.start_Manager(url_q,result_q)
    #创佳三个进程，url管理，数据提取，数据存储
    url_manager_proc = Process(target=node.url_manager_proc,args=(url_q,conn_q,root_url,))
    result_solve_proc = Process(target=node.result_solve_proc,args=(result_q,conn_q,store_q,))
    store_proc = Process(target=node.store_proc,args=(store_q,))
    manager_run = Process(target=manager.start)


    manager.start()
    # manager_run.start()
    time.sleep(5)
   # manager.join()
    # store_proc.start()
    # print("1 start")
    # time.sleep(5)
    # url_manager_proc.start()
    # print("2 start")
    # time.sleep(10)
    # # result_solve_proc.start()
    # # print("3 start")
    # # time.sleep(15)
    # print("4 start")

