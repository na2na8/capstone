import csv
import urllib.request
import pandas as pd

def downpng(dataframe,category) :
    length = dataframe.shape[0]
    for i in range(0, length) :
        URL = 'http:' + dataframe.loc[i, 'image']
        path = 'E:/emart3_cleaned' +category+'_image/'+str(dataframe.loc[i, 'product']) + '.png'
        urllib.request.urlretrieve(URL, path)

dataframe = ['C:/Users/na2na/Desktop/emart3_cleaned_치즈.csv', 'C:/Users/na2na/Desktop/emart3_cleaned_우유.csv',
            'C:/Users/na2na/Desktop/emart3_cleaned_소스류.csv', 'C:/Users/na2na/Desktop/emart3_cleaned_빵.csv']
category = ['치즈', '우유', '소스류', '빵']


for i in range(0, 4) :
    csv_file = pd.read_csv(dataframe[i])
    downpng(csv_file, category[i])