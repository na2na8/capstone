from selenium import webdriver
from bs4 import BeautifulSoup
import re
import requests
import csv

#특수기호 제거, 언더바->스페이스, 곱하기 기호
def cleanText(readData):
    text = re.sub('[-=,./\\(\)\[\]\{\}<>?:~₩!@#$%^&●]', '', readData)
    text = text.replace("_", " ")
    text = text.replace("x", "*")
    text = text.replace("×", "*")
    return text

def cleanName(readData):
    name = cleanText(readData).upper()
#     if '*' in name :
#         i = readData.find('*')
#         name = readData[:i]
    
    #[괄호]와 그 안의 내용 제거
    name = re.sub('\[[^)]*\]', '', name)
    return name

# 반올림
def _round(price) :
    rounded_price = round(float(price)/100)
    rounded_price = rounded_price*100
    return rounded_price

# Chrome driver // 경로
driver = webdriver.Chrome('/Users/na2na/Downloads/chromedriver_win32/chromedriver')
# waiting web source loading 3 sec.
driver.implicitly_wait(3)

# url
url = "http://emart.ssg.com/category/main.ssg?dispCtgId="

emart_category_id = {
    "0006110014" : "과일", "0006110003" : "과일", "0006110004" : "과일", "0006110005" : "과일", "0006110006" : "과일",
    "0006110007" : "과일", "0006110008" : "과일", "0006110009" : "과일", "0006110011" : "과일", "0006110012" : "과일"
}


with open('emart.csv', 'w', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerow(['item', 'product', 'price', 'image'])

#우선 e마트만
for i in range(5, 6) :
    category_id = list(emart_category_id.keys())[i]
    new_url = url + category_id
    driver.get(new_url)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # 마지막 페이지 찾기
    pagenum_class = soup.find("div", {"class" : "com_paginate notranslate"})
    pagenum_list = list(pagenum_class.find_all("a", {"href" : "#"}))
    page_len = len(pagenum_list)
    pagenum = 0
    if page_len == 11 :
        left = pagenum_list[10]["onclick"].find("(")
        right = pagenum_list[10]["onclick"].find(")")
        pagenum = int(pagenum_list[10]["onclick"][left+1:right])
    else :
        left = pagenum_list[page_len-1]["onclick"].find("(")
        right = pagenum_list[page_len-1]["onclick"].find(")")
        pagenum = int(pagenum_list[page_len-1]["onclick"][left+1:right])

    for j in range(1, pagenum+1) :
        new_url = new_url + "&page=" + str(j)
        
        find_class = soup.find("div", {"class" : "cunit_lst_v"})
        product = find_class.find_all("img", {"class" : "i1"})
        price = soup.find_all("em", {"class" : "ssg_price"})

        #csv로 저장    
        with open('emart.csv', 'a', encoding='UTF-8') as file:
            writer = csv.writer(file, delimiter=',')
            length = len(product)
            for k in range(0, length) :
                name = cleanName(product[k]["alt"])
                
                img = product[k]["src"]
                price_ = price[k].text
                price_ = int(re.sub('[,]' , '', price_))
                price_ = _round(price_)

                category_num = list(emart_category_id.values())[i]
                writer.writerow([category_num, name, price_, img])

# 저장된 파일 pd로 읽기
import pandas as pd
data = pd.read_csv('emart.csv')
data