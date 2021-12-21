from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import re # 정규표현식
import csv

#특수기호 제거, 언더바->스페이스, 곱하기 기호
def cleanText(readData):
    text = re.sub('[-=,./\\(\)\[\]\{\}<>?:~₩!@#$%^&●]', '', readData)
    text = text.replace("_", " ")
    text = text.replace("x", "*")
    text = text.replace("×", "*")
    return text

#상품 명 중 '*' 뒤의  판별
def delmul(readData):
    i = readData.find('*')
    return readData[:i]
# 이미지 다운받는 코드
# urllib.request.urlretrieve(url, savename)

# url 작성
web_url = "http://www.lottemart.com/category/categoryList.do?CategoryID=C001014400010001"

# web_url에 원하는 웹의 URL 넣기
with urllib.request.urlopen(web_url) as response :
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')

    #롯데마트의 경우 class="wrap-prod-list"에 사진과 함께 제품명 들어있음.
    find_class = soup.find("div", {"class" : "wrap-prod-list"})
    product = find_class.find_all("img", {"width" : "208"})
    # product_name = re.search('alt=".*"', product)
    price = soup.find_all("span", {"class" : "num-n"})
    # image = find_class.find_all("img", {"width" : "208"})

#csv로 저장
with open('홍삼.csv', 'w', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerow(['ID', 'item', 'product', 'price', 'image'])

    length = len(product)
    for i in range(0, length) :
        name = cleanText(product[i]["alt"]).upper()
        if '*' in name :
            name = delmul(name)
        img = product[i]["src"]
        price_ = price[i].text
        writer.writerow([i, "category", name, price_, img])

# 저장된 파일 pd로 읽기
import pandas as pd
data = pd.read_csv('홍삼.csv')
data