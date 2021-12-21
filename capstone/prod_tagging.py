import csv
import pandas as pd
import numpy as np
import re
import pyjosa
import random

item_list = ['우유', '치즈', '사탕', '아이스크림', '과자', '김치']

# 어절 태깅
def tagging_words(product) :
    words_tagging = []
    splitted= product.split(" ")
    
    len_splitted = len(splitted)-1
    # splitted 사이사이에 " " 채워주기
    while len_splitted > 0 :
        splitted.insert(len_splitted, " ")
        len_splitted -= 1
        
    len_splitted = len(splitted)-1
    # 태깅. 완벽하지 않아 수동으로 체크해 주어야 함. 
    # (ex : 치즈 케이크인경우 치즈를 품목으로 생각하기 때문에 이를 바꾸어 주어야 함)
    for item in splitted :
        if item in item_list :
            words_tagging.append('PRDG_B')
        else :
            # 품목명이 아닌 경우 모두 PRD_I를 태깅해 줌.
            words_tagging.append('PRD_I')
    # 품목명이 있을 경우 ' '의 위치에 '-'를 붙이는 경우
    try :
        # 품목명 위치 찾기
        where_prdg = words_tagging.index('PRDG_B')
        if where_prdg != 0 and splitted[where_prdg-1] == ' ' :
            words_tagging[where_prdg -1] = '-'
        if (where_prdg != len_splitted) and splitted[where_prdg+1] == ' ':
            words_tagging[where_prdg +1] = '-'
    except :
        pass
    
    try :
        # 처음 PRD_I를 찾은 곳에 PRD_B로 바꿔주기
        find_prd_b = words_tagging.index('PRD_I')
        words_tagging[find_prd_b] = 'PRD_B'
    except :
        pass
    return splitted, words_tagging
    

# 음절 태깅
def tagging_syllables(product, words, words_tagging) :
    product_length = len(product)
    syllables = []
    syl_tagging = []
    # 음절단위로 product 쪼개기
    for i in range(0, product_length) :
        syllables.append(product[i])

    for word_idx in range(0, len(words)) :
        words_length = len(words[word_idx])
        # 어절 태깅이 PRD_B일 때
        if words_tagging[word_idx] == 'PRD_B' :
            for j in range(0,words_length) :
                 # PRD_B 단어의 첫 음절만 PRD_B
                if j == 0 :
                    syl_tagging.append('PRD_B')
                else :
                    syl_tagging.append('PRD_I')
        # 어절 태깅이 PRD_I일 때
        elif words_tagging[word_idx] == 'PRD_I' :
            for j in range(0, words_length) :
                syl_tagging.append('PRD_I')
        # 어절 태깅이 PRDG_B일 때
        elif words_tagging[word_idx] == 'PRDG_B' :
            for j in range(0,words_length) :
                if j == 0 :
                    syl_tagging.append('PRDG_B')
                else :
                    syl_tagging.append('PRDG_I')
        else :
            for j in range(0, words_length) :
                syl_tagging.append('-')
        
    return syllables, syl_tagging


def choose_plural(filename) :
    data = pd.read_csv(filename)
    length = data.shape[0]
    # 복수 2개를 랜덤 두 개 선택
    num1 = random.randrange(0, length)
    num2 = random.randrange(0, length)
    # 중복 제거
    while num2 == num1 :
        num2 = random.randrange(0,length)
    name1 = str(data.loc[num1, 'product'])
    name2 = str(data.loc[num2, 'product'])
    
    plural = pyjosa.replace_josa(name1 + "(와)과 " + name2)
    
    words = []
    words_tagging = []
    syllables = []
    syllables_tagging = []
    
    len_name1 = len(name1)
    # 조사(와, 과) 위치
    josa = plural[len_name1]
    josa2 = ''
    if josa == '과' :
        josa2 = '이랑'
    elif josa == '와' :
        josa2 = '랑'
    
    # ------------- case 1 조사 : 와/과, case 2 조사 : 랑/이랑, case 3 조사 : 조사없이 그냥 붙을 때 -------------- #
    # 어절 태깅
    name1_splitted, name1_words_tagging = tagging_words(name1)
    for i in range(0, len(name1_splitted)) :
        words.append(name1_splitted[i])
    
    for i in range(0, len(name1_words_tagging)) :
        words_tagging.append(name1_words_tagging[i])
    
    case = random.randrange(1,4)
    print(case)
    
    if case == 1 :
        words.append(josa)
        words.append(' ')    
        # 조사 태깅
        words_tagging.append('-')
        # 띄어쓰기 태깅
        words_tagging.append('-')
    elif case == 2 :
        words.append(josa2)
        words.append(' ')
        # 조사 태깅
        words_tagging.append('-')
        # 띄어쓰기 태깅
        words_tagging.append('-')
    else :
        # 조사 X
        words.append(' ')
        # 띄어쓰기 태깅
        words_tagging.append('-')
        
    
    name2_splitted, name2_words_tagging = tagging_words(name2)
    for i in range(0, len(name2_splitted)) :
        words.append(name2_splitted[i])
    for i in range(0, len(name2_words_tagging)) :
        words_tagging.append(name2_words_tagging[i])
    
    new_plural = ''
    for j in range(0, len(words)) :
        new_plural = new_plural + words[j]
    # 음절 태깅
    syllables, syllables_tagging = tagging_syllables(new_plural, words, words_tagging)
    
    
    return new_plural, words, words_tagging, syllables, syllables_tagging


data = pd.read_csv('C:/Users/na2na/capstone/random_prod_without_dupl.csv')
length = data.shape[0]

with open('C:/Users/na2na/capstone/random_prod_tagging.csv', 'w', encoding = 'UTF-8') as file :
    wtr = csv.writer(file, delimiter = ',')   
    wtr.writerow(['product', 'words', 'words_tagging', 'syllables', 'syllables_tagging'])

    for line in range(0, length) :
        product = data.loc[line, 'product']
        words, words_tagging = tagging_words(line, product)
        syllables, syl_tagging = tagging_syllables(product, words, words_tagging)
        wtr.writerow([product, words, words_tagging, syllables, syl_tagging])

# 복수 추가
# 데이터 길이 갱신
length = data.shape[0]
with open('C:/Users/na2na/capstone/random_prod_tagging.csv', 'a', encoding = 'UTF-8') as file :
    wtr = csv.writer(file, delimiter = ',')

    for i in range(0, 800) :
        product, words, words_tagging, syllables, syllables_tagging = choose_plural(file)
        wtr.writerow([product, words, words_tagging, syllables, syllables_tagging])
        
