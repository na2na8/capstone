from selenium import webdriver
from bs4 import BeautifulSoup
import re
import csv
import math

driver = webdriver.Chrome('/Users/na2na/Downloads/chromedriver_win32/chromedriver')
driver.implicitly_wait(3)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')


url = "http://www.lottemart.com/category/categoryList.do?CategoryID=C001014400010001"

driver.get(url)

page_info = soup.find("a", {"class" : "page-last"})
if page_info == 'None' :
    print("none")
print(page_info)
print(type(page_info))