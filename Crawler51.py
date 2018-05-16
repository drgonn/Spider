#!/usr/bin/env python3
# -*- coding=UTF-8 -*-

#爬取51job上招聘python工程师的信息

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import codecs




class Crawler51(object):
    def get_job(self,driver,job):
        ele_name= driver.find_element_by_name('loginname')
        ele_pwd = driver.find_element_by_name('password')
        ele_login = driver.find_element_by_id('login_btn')

        ele_name.send_keys('dronnn@163.com')
        ele_pwd.send_keys('7811175yy')
        ele_login.click()
        ele_login.click()

        # time.sleep(5)


        ele_select = driver.find_element_by_id('kwdselectid')
        ele_search = driver.find_elements_by_xpath('//button')[1]
        ele_select.send_keys(job)
        ele_search.click()
        page_num = 1
        while True:

            try:
                element = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.ID,"resultList")))
            except Exception as e:
                print(e)


            htm_cont = driver.page_source
            # print(htm_cont)
            soup=BeautifulSoup(htm_cont,'html.parser')
            # print(soup)
            infos = soup.find(id="resultList").find_all(class_='el')
            f = codecs.open(job+'.txt','a','utf-8')

            for info in infos:
                f.write("-_- "*10+"\n")
                content=info.get_text().strip()
                for line in [ln for ln in content.splitlines() if ln.strip()]:
                    f.write(line)
                    f.write('\r\n')
            f.close()
            ele_next = driver.find_elements_by_class_name("bk")[1]
            time.sleep(1)

            try:
                next = WebDriverWait(driver,20).until(EC.visibility_of(ele_next.find_element_by_tag_name('a')))
                page_num += 1
                ele_next.click()
            except Exception as e:
                print(e,111111111111118)
                break



    def crawl(self,root_url,job):
        driver = webdriver.Firefox()
        # driver.maximize_window()
        driver.set_page_load_timeout(50)
        driver.implicitly_wait(10)
        driver.get(root_url)

        self.get_job(driver,job)



if __name__=="__main__":
    spider = Crawler51()
    spider.crawl("https://login.51job.com/login.php?lang=c&url=http%3A%2F%2Fwww.51job.com%2F",'python')

















