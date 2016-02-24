# coding = utf-8
import os
from selenium import webdriver

fp = webdriver.FirefoxProfile(os.path.expanduser('~/Library/Application Support/Firefox/Profiles/0hn8nym4.default/'))
fp.set_preference("javascript.enabled",False)
browser = webdriver.Firefox(firefox_profile=fp)
browser.get('https://www.google.com.tw/')
search_box = browser.find_element_by_name('q')
search_box.send_keys('ChromeDriver')
search_box.submit()
aTag =  browser.find_element_by_tag_name('a')
print search_box.get_attribute("href")



