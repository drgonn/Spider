#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

import time,random


class send_resume():



	def crawl(self,root_url):
		driver = webdriver.Firefox()
		driver.set_page_load_timeout(50)
		driver.implicitly_wait(10)
		driver.get(root_url)
		self.send(driver)


	def send(self,driver):
		ele_phone = driver.find_element_by_name("account")
		ele_pwd = driver.find_element_by_name("password")
		ele_validate = driver.find_element_by_name("captcha")
		
		# ele_login = driver.find_element_by_xpath("")


		ele_phone.send_keys('18666821287')
		ele_pwd.send_keys("7811175yy")
		vali = input("输入验证马: ")
		ele_validate.send_keys(vali)
		time.sleep(0.5)
		ele_validate.send_keys(Keys.RETURN)

		count = 0


		try:
			element = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.ID,"async-sider")))
		except Exception as e:
			print(e)

		#处理下拉菜单

		# time.sleep(1)
		# print("start")
		# ele_city = driver.find_element_by_class_name("city-sel")
		# time.sleep(2)
		# ele_city.click()
		# time.sleep(5)
		# drop1 = driver.find_element_by_class_name("dorpdown-province")
		# sz1 = drop1.find_elements_by_xpath('.//li[@class=""]')[15]
		# sz1.click()

		# time.sleep(2)
		# ele_city.click()
		# time.sleep(2)	
		# print("start2")

		ele_job=driver.find_element_by_name("query")
		ele_job.send_keys("python")
		ele_job.send_keys(Keys.RETURN)
		try:
			print("!"*12)
			element = WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.ID,"filter-box")))
		except Exception as e:
			print(e)

		time.sleep(3)

		ele_sz = driver.find_element_by_xpath(".//a[@ka='sel-city-101280600']")
		ele_sz.click()

		while True:

			time.sleep(5)

			zw= driver.find_element_by_class_name("job-list")
			ele_zws =zw.find_elements_by_class_name("job-title")

			for ele_zw in ele_zws:
				ele_zw.click()
				windows = driver.window_handles
				driver.switch_to.window(windows[1])

				try:
					element = WebDriverWait(driver,20).until(EC.presence_of_element_located(By.linkText,"沟通"))
				except Exception as e:
					print(e)


				touguo = True

				try:
					driver.find_element_by_partial_link_text("继续沟通")
				except:
					count += 1
					print("投递简历%s份。"%count)
					touguo = False

				if not touguo:
					send= driver.find_elements_by_xpath(".//div[@class='detail-op']")[1].find_element_by_tag_name("a")
					send.click()
					time.sleep(5)
					print("guanbibiaoqian")

					time.sleep(5)
					print("send OK")
					driver.close()
					driver.switch_to.window(windows[0])
				else:
					driver.close()
					driver.switch_to.window(windows[0])

			ele_next = driver.find_element_by_class_name("next")
			
			if ele_next.get_attribute("href") == "javascript:;":
				print("此次共投递简历 %s 份。" %count)
				break


			ele_next.click()


			try:
				element = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.ID,"async-sider")))
			except Exception as e:
				print(e,4)




time.sleep(10)




		# drop = driver.find_element_by_class_name("dorpdown-city")
		# sz = drop.find_elements_by_xpath('.//li[@class="cur"]')[4]
		# sz.click()



		# select = driver.find_element_by_class_name("city-box")
		# all_citys =select.find_elements_by_tag_name("li")
		# select.select_by_index(index)
		# print(select.options)








if __name__=="__main__":

	spider = send_resume()
	spider.crawl("https://login.zhipin.com/?ka=header-login")
