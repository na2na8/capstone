# txt 파일 미리 생성
fw = open('C:/Users/na2na/capstone/word_tagging.txt', 'w')
fw_no_num = open('C:/Users/na2na/capstone/word_tagging_no_num.txt', 'w')
fs = open('C:/Users/na2na/capstone/syllable_tagging.txt', 'w')
fs_no_num = open('C:/Users/na2na/capstone/syllable_tagging_no_num.txt', 'w')

fw.close()
fw_no_num.close()
fs.close()
fs_no_num.close()

import csv
import pandas as pd
import numpy as np

# 시험삼아 학습시켜 보는데, 앞에 index가 있으면 학습이 잘 안 되는 것을 알게 되어 index있는 txt와 없는 txt를 같이 만들어 줌.


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

# 문장 어절단위 태깅을 txt 파일로 저장
def word_tagging_to_txt(words, words_tagging) :
    f = open('C:/Users/na2na/capstone/word_tagging.txt', 'a')
    f_no_num = open('C:/Users/na2na/capstone/word_tagging_no_num.txt', 'a')
    for idx in range(1, len(words)+1) :
        data = "%d\t%s\t%s\n" % (idx, words[idx-1], words_tagging[idx-1])
        data_no_num = "%s\t%s\n" % (words[idx-1], words_tagging[idx-1])
        f.write(data)
        f_no_num.write(data_no_num)
    data= "\n"
    f.write(data)
    f_no_num.write(data)
    f.close()
    f_no_num.close()

# 문장 음절단위 태깅을 txt 파일로 저장    
def syllable_tagging_to_txt(syl, syl_tagging) :
    f = open('C:/Users/na2na/capstone/syllable_tagging.txt', 'a')
    f_no_num = open('C:/Users/na2na/capstone/syllable_tagging_no_num.txt', 'a')
    for idx in range(1, len(syl)+1) :
        data = "%d\t%s\t%s\n" % (idx, syl[idx-1], syl_tagging[idx-1])
        data_no_num = "%s\t%s\n" % (syl[idx-1], syl_tagging[idx-1])
        f.write(data)
        f_no_num.write(data_no_num)
    data = '\n'
    f.write(data)
    f_no_num.write(data)
    f.close()
    f_no_num.close()

    
data = pd.read_csv('C:/Users/na2na/capstone/sentence_tag_real_final.csv')
length = data.shape[0]

for i in range(0, length) :
    words = str_to_list(data.loc[i, 'words'])
    words_tagging = str_to_list(data.loc[i, 'words_tag'])
    word_tagging_to_txt(words, words_tagging)
    syllables = str_to_list(data.loc[i, 'syllables'])
    syllables_tagging = str_to_list(data.loc[i, 'syllables_tag'])
    syllable_tagging_to_txt(syllables, syllables_tagging)