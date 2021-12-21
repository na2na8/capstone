import random
import re
import csv
from konlpy.corpus import kobill
from konlpy.tag import Twitter
import pandas as pd


item_list = ['우유', '치즈', '사탕', '아이스크림', '과자', '김치']

t= Twitter()
# tags_ko = t.pos("카라멜아몬드초콜릿초코아몬드")
    
# 상품명 일부를 생략해 줌.
def drop_part_of_product(splitted, at_least) :
    length = len(splitted)
    # num : 뺄 단어의 개수
    num = random.randrange(0, length-at_least+1)
    # rm_list : 뺄 단어의 위치 리스트
    rm_list = []
    if num != 0 :
        rm_num = random.randrange(0,num+1)
        rm_list.append(rm_num)
        for i in range(0, num-1) :
            rm_num = random.randrange(0,num+1)
            #중복되지 않게
            while(rm_num in rm_list) :
                rm_num = random.randrange(0,num+1)
            rm_list.append(rm_num)
        rm_list.sort()
        while len(rm_list) != 0 :
            to_be_removed = rm_list.pop()
            splitted.pop(to_be_removed)
    else :
        pass
        
    return splitted

# 조합 방법 정하는 코드
def define_combination(item, name, attr) :
    # case : 
    case = random.randrange(1,4)
    splitted = name.split(" ")
    # 4. 상품명 일부와 품목명 조합 ex) 서울우유 1000ML -> 우유 1000ML
    if item in item_list and case == 3 :
        result = item + " " + attr
        return result
    elif (item not in item_list) and case == 3 :
        while case == 3 :
            case = random.randrange(1,4)
    
    # 1. 상품명 일부 생략 ex) 하겐다즈 그린티 아몬드 멀티바 -> 하겐다즈 아몬드
    elif case == 1 :
        if len(splitted) > 1 :
            splitted = drop_part_of_product(splitted, at_least = 2) # 최소 2개 이상 남기기
        result = " ".join(splitted)
        return result
    
    # 2. 상품명 일부과 품목명 조합 ex) 매일유업 매일우유 저지방 -> 저지방 우유
    # 5. 상품명 일부와 품목명 조합 ex) 하겐다즈 바닐라 카라멜아몬드초콜릿초코아몬드 미니바 40ML -> 바닐라 아이스크림
    elif case == 2 :
        splitted = drop_part_of_product(splitted, at_least = 1)
        for i in range(len(splitted)) :
            if len(splitted[i]) > 4 :
                # 한국어 형태소로 tagging
                tags_ko = t.pos(splitted[i])
                # 대표로 지정할 형태소 random하게 골라줌.
                random_num = random.randrange(0, len(tags_ko))
                random_name = tags_ko[random_num][0]
                splitted[i] = random_name
        result = " ".join(splitted)
        # 품목이 item_list안에 없고 품목이 상품 이름에 포함될 경우
        if (item not in item_list) and (item in result) :
            return result
        # 품목이 item_list안에 있고 품목이 상품 이름에 없을 경우
        elif (item in item_list) and (item not in result) :
            result = result + " " + item
            return result
        # 제외한 모든 경우
        else :
            return result
    # 3. 상품명 일부 생략 및 변형 ex) 매일우유 매일 바이오 플레인 -> 매일 바이오 플레인 맛
    # 3번은 수동으로 맛을 붙여주기로 함. 컴퓨터는 딥러닝을 하지 않는 이상 해당 글자의 의미를 파악할 수 없기 때문 
                    
                
# 결과가 완벽하지 않아 수동으로 정제 해주어야 함
data = pd.read_csv('C:/Users/na2na/capstone/random.csv')
length = data.shape[0]

with open('C:/Users/na2na/capstone/random_prod.csv', 'w', encoding = 'UTF-8') as file :
    wtr = csv.writer(file, delimiter=",")
    wtr.writerow(['product'])

with open('C:/Users/na2na/capstone/random_prod.csv', 'a', encoding = 'UTF-8') as file :
    wtr = csv.writer(file, delimiter = ',')    
    for i in range(0,length) :
        name = data.loc[i, 'product']
        item = data.loc[i, 'item']
        attr = data.loc[i, 'unitmark']
        ans = define_combination(item, name, attr)
        if ans == None :
            ans = name

        wtr.writerow([ans])
        print(i, ans)

