#!/usr/bin/env python3
# -*- coding=UTF-8 -*-

#爬取去哪儿网当天上海酒店信息

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import codecs

driver = webdriver.Firefox()
driver.set_window_size(1080, 1080)
driver.get("http://hotel.qunar.com/")
assert '去哪儿网' in driver.title

toCity = '上海'

# ele_toCity = driver.find_element_by_xpath("//div[@id='js_searchbox_flight']/input[3]")

# ele_hotel = driver.find_element_by_xpath(".//*[@data-for='hotel']")
# ele_hotel.click()
# time.sleep(10)
#
ele_toCity = driver.find_element_by_id('toCity')
ele_fromDate = driver.find_element_by_name('fromDate')
ele_search = driver.find_element_by_class_name(
    'search-button')



ele_toCity.clear()
print(11111)
ele_toCity.send_keys(toCity)
ele_toCity.click()
ele_search.click()
# elem.send_keys(Keys.RETURN)


try:
    WebDriverWait(driver,10).until(EC.title_contains(toCity))
except Exception as e:
    print(e)
    # break
time.sleep(5)

js = "window.scrollTo(0,document.body.scrollHeight);"
driver.execute_script(js)
time.sleep(5)
htm_const=driver.page_source


soup = BeautifulSoup(htm_const,'html.parser')
infos = soup.find_all(class_='item_hotel_info')
f = codecs.open(toCity+'.html','a')
for info in infos:
    f.write('--'*20)
    content = info.get_text().replace(" ","").replace("\t","").strip()
    for line in [ln for ln in content.splitlines() if ln.strip()]:
        f.write(line)
        f.write('\r\n')
    print(content)
    f.close
