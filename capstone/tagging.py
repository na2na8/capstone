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


def str_to_list(words):
    words=words.replace('\'','')
    words=words.replace('[','')
    words=words.replace(']','')
    words=words.split(',')
    for i in range(len(words)) :
        words[i] = words[i].strip()
        if len(words[i]) == 0 :
            words[i] = ' '
    return words


# filename : 태깅 된 csv
def choose_plural(filename, length) :
    data = pd.read_csv(filename)
    # 복수 2개를 랜덤 두 개 선택
    num1 = random.randrange(0, length)
    num2 = random.randrange(0, length)
    # 중복 제거
    while num2 == num1 :
        num2 = random.randrange(0,length)
    # 상품 이름
    name1 = str(data.loc[num1, 'product'])
    name2 = str(data.loc[num2, 'product'])
    
    # 상품 어절
    name1_words = str_to_list(data.loc[num1, 'words'])
    name2_words = str_to_list(data.loc[num2, 'words'])
    
    # 상품 어절 태깅
    name1_words_tagging = str_to_list(data.loc[num1, 'words_tagging'])
    name2_words_tagging = str_to_list(data.loc[num2, 'words_tagging'])
    
    # 상품 음절
    name1_syllables = str_to_list(data.loc[num1, 'syllables'])
    name2_syllables = str_to_list(data.loc[num2, 'syllables'])
    
    # 상품 음절 태깅
    name1_syllables_tagging = str_to_list(data.loc[num1, 'syllables_tagging'])
    name2_syllables_tagging = str_to_list(data.loc[num2, 'syllables_tagging'])
    
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
    
    # ------------------------------------------------------------------------------------------------------------ #
    # name 1
    # 어절
    for i in range(0, len(name1_words)) :
        words.append(name1_words[i])
    # 태그된 어절
    for i in range(0, len(name1_words_tagging)) :
        words_tagging.append(name1_words_tagging[i])
    
    # 음절
    for i in range(0, len(name1_syllables)) :
        syllables.append(name1_syllables[i])
    # 태그된 음절
    for i in range(0, len(name1_syllables_tagging)) :
        syllables_tagging.append(name1_syllables_tagging[i])
    
    # ------------------------------------------------------------------------------------------------------------ #
    # ------------- case 1 조사 : 와/과, case 2 조사 : 랑/이랑, case 3 조사 : 조사없이 그냥 붙을 때 -------------- #
    case = random.randrange(1,4)
    
    # 와/과
    if case == 1 :
        words.append(josa)
        words.append(' ')    
        # 조사 어절 태깅
        words_tagging.append('-')
        # 띄어쓰기 어절 태깅
        words_tagging.append('-')
        # 조사 음절 태깅
        syllables.append(josa)
        syllables.append(' ')
        # 띄어쓰기 음절 태깅
        syllables_tagging.append('-')
    # 이랑/랑
    elif case == 2 :
        words.append(josa2)
        words.append(' ')
        # 조사 어절 태깅
        words_tagging.append('-')
        # 띄어쓰기 어절 태깅
        words_tagging.append('-')
        len_josa2 = len(josa2)
        # 조사 음절 태깅
        for i in range(0, len_josa2) :
            syllables.append(josa2[i])
        syllables.append(' ')
        # 띄어쓰기 음절 태깅
        for i in range(0, len_josa2) :
            syllables_tagging.append('-')
        syllables_tagging.append('-')
    # 조사 X
    else :
        # 띄어쓰기
        words.append(' ')
        # 띄어쓰기 태깅
        words_tagging.append('-')
        # 음절 띄어쓰기
        syllables.append(' ')
        # 음절 띄어쓰기 태깅
        syllables_tagging.append('-')
    
    # ------------------------------------------------------------------------------------------------------------ #
    # name 2
    # 어절
    for i in range(0, len(name2_words)) :
        words.append(name2_words[i])
    # 태그된 어절
    for i in range(0, len(name2_words_tagging)) :
        words_tagging.append(name2_words_tagging[i])
    
    # 음절
    for i in range(0, len(name2_syllables)) :
        syllables.append(name2_syllables[i])
    # 태그된 음절
    for i in range(0, len(name2_syllables_tagging)) :
        syllables_tagging.append(name2_syllables_tagging[i])
        
    # ------------------------------------------------------------------------------------------------------------ #
    
    # case에 맞게 
    new_plural = ''
    for j in range(0, len(words)) :
        new_plural = new_plural + words[j]
    
    
    return new_plural, words, words_tagging, syllables, syllables_tagging



# Part마다 주석 처리 or 해제 하면서 실행하면 됩니다.


# Part1
# 태깅 작업 -----------------------------------------------------------------------------------------------
# data : 정제된 상품명을 변형한 csv를 사용
# data = pd.read_csv('C:/Users/na2na/capstone/random_prod_without_dupl2.csv')
# length = data.shape[0]

# with open('C:/Users/na2na/capstone/random_prod_tagging2.csv', 'w', encoding = 'UTF-8') as file :
#     wtr = csv.writer(file, delimiter = ',')   
#     wtr.writerow(['product', 'words', 'words_tagging', 'syllables', 'syllables_tagging'])

#     for line in range(0, length) :
#         product = data.loc[line, 'product']
#         words, words_tagging = tagging_words(product)
#         syllables, syl_tagging = tagging_syllables(product, words, words_tagging)
#         wtr.writerow([product, words, words_tagging, syllables, syl_tagging])






# Part2
# 태깅된 csv에 복수 추가-----------------------------------------------------------------------------------
# 데이터 길이 갱신
# data : 태깅을 완벽하게(수동으로까지) 완료한 csv를 사용
# data = pd.read_csv('C:/Users/na2na/capstone/prod_tagging_.csv')
# length = data.shape[0]
# # 태깅이 올바르게 된 것을 가지고 돌려야 함. csv파일의 태깅된 것을 활용하기 때문
# with open('C:/Users/na2na/capstone/prod_tagging_.csv', 'a', encoding = 'UTF-8') as file :
#     wtr = csv.writer(file, delimiter = ',')
    
#     # 복수 상품 생성은 원하는 만큼. range(0, 원하는 만큼) -> 중복된 것이 나타날 수 있음.
#     for i in range(0, 1619) :
#         product, words, words_tagging, syllables, syllables_tagging = choose_plural('C:/Users/na2na/capstone/prod_tagging_.csv', length)
#         wtr.writerow([product, words, words_tagging, syllables, syllables_tagging])

#----------------------------------------------------------------------------------------------------------

        
        
        
# Part3      
# 문장 어절 태깅 -> 음절태깅 --------------------------------------------------------------------------------
# data : 문장 태깅된 csv를 사용
# 음절로 바꾸는 방법이 상품명 처리와 같은 방식을 사용
data = pd.read_csv('C:/Users/na2na/capstone/sentence_tag_final.csv')
length = data.shape[0]

with open('C:/Users/na2na/capstone/sentence_tag_final.csv', 'a', encoding = 'UTF-8') as file :
    wtr = csv.writer(file, delimiter = ',')
    syl = []
    syl_tag = []
    for line in range(0, length) :
        print(line)
        product = data.loc[line, 'sentence']
        words = str_to_list(data.loc[line, 'words'])
        words_tagging = str_to_list(data.loc[line, 'words_tag'])
        syllables, syl_tagging = tagging_syllables(product, words, words_tagging)
        syl.append(syllables)
        syl_tag.append(syl_tagging)
    data['syllables'] = syl
    data['syllables_tag'] = syl_tag

data.to_csv('C:/Users/na2na/capstone/sentence_tag_real_final.csv')

#----------------------------------------------------------------------------------------------------------