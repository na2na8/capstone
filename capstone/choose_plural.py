import random
import csv
import pandas as pd
import pyjosa

# 복수의 상품명 추출
def choose_plural(filename) :
    data = pd.read_csv(filename)
    length = data.shape[0]
    num1 = random.randrange(0, length)
    num2 = random.randrange(0, length)
    # 중복 제거
    while num2 == num1 :
        num2 = random.randrange(0,length)
    name1 = data.loc[num1, 'product']
    name2 = data.loc[num2, 'product']
    
    with open(filename, 'a', encoding = 'UTF-8') as file :
        wtr = csv.writer(file, delimiter = ',') 
        plural = pyjosa.replace_josa(str(name1) + "(와)과 " + str(name2))
        wtr.writerow([plural])

for i in range(0, 817) :
    choose_plural('C:/Users/na2na/capstone/random_prod_without_dupl.csv')