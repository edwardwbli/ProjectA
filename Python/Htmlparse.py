#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
import time
import codecs
from selenium import webdriver
from bs4 import BeautifulSoup

class Chromwebdriver(object):
    SearchEgURL = 'https://www.google.com/'
    def __init__(self):
        # Optional argument, if not specified will search path.
        self.driver = webdriver.Chrome('/Users/wangshidi/Downloads/chromedriver')  
        
    def Rosisearch(self,keyword):
        self.keyword = keyword
        

        # launch Chrome by getting URL
        self.driver.get(self.SearchEgURL)

        # locate search_box 
        self.search_box = self.driver.find_element_by_name('q')
        self.search_box.send_keys(self.keyword)
        self.search_box.submit()
        # time.sleep(5) # Let the user actually see something!

        # Optional Obtainning full page_source
        # return self.driver.page_source
        # link = driver.find_element_by_tag_name("a")
        # print link
        return self.driver
        # Close Chrome
        #self.driver.close()
        #driver.quit()
    def driverclose(self):
        self.driver.close()

    def driverdir(self):
        return dir(self.driver)

    def resultlink(self):
        pass

Searchany = Chromwebdriver()
Searchany.Rosisearch("ROSI")  
print Searchany.driverdir()

