from selenium import webdriver
from bs4 import BeautifulSoup
import re
import csv
import math

#특수기호 제거, 언더바->스페이스, 곱하기 기호
def cleanText(readData):
    text = re.sub('[-=,./\\(\)\[\]\{\}<>?:~₩!@#$%^&●]', '', readData)
    text = text.replace("_", " ")
    text = text.replace("x", "*")
    text = text.replace("×", "*")
    return text

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
url = "http://www.homeplus.co.kr/app.exhibition.category.Category.ghs?comm=category.list&cid="


homeplus_category_id = {
    "60003" : "과일", "60005" : "과일", "60007" : "과일", "60009" : "과일", "60011" : "과일",
    "60013" : "과일", "60015" : "과일", "60017" : "과일", "60019" : "과일", "60021" : "과일"
}

with open('homeplus.csv', 'w', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerow(['item', 'product', 'price', 'image'])

#우선 e마트만
for i in range(0, 1) :
    category_id = list(homeplus_category_id.keys())[i]
    new_url = url + category_id
    driver.get(new_url)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    while(True) : # Exception이 나올 때까지 더보기 버튼 눌러서 모두 펼친 다음, Exception 나오면 크롤링 하고 while문 빠져나옴.
        try :
            driver.find_element_by_class_name('more').click()
        except :
            find_class = soup.find("div", {"id" : "ui-thumb-type"})
            product = find_class.find_all("img", {"height" : "176"}) # img는 ["src"], product 이름은 ["alt"]
            price = soup.find_all("strong", {"class" : "buy"})
            length = len(product)
            print(length)
            print(len(price))
            
            with open('homeplus.csv', 'a', encoding='UTF-8') as file :
                writer = csv.writer(file, delimiter=',')
                
                for k in range(0, length) :
                    name = cleanText(product[k]["alt"])
                    img = product[k]["src"]
                    price_ = int(cleanText(price[k].text))
                    price_ = _round(price_)
                    
                    category_num = list(homeplus_category_id.values())[i]
                    writer.writerow([category_num, name, price_, img])
                
            break;
        
# 저장된 파일 pd로 읽기
import pandas as pd
data = pd.read_csv('homeplus.csv')
data