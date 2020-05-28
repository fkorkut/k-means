import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import copy
    
 
from sklearn.preprocessing import Imputer
veriler = pd.read_csv('veri.csv')
 
df = pd.DataFrame({
   'x': veriler.iloc[:,0].values,
  	'y': veriler.iloc[:,1].values
})

print(df.values)
def merkezolustur(k):
    merkezler = {
            i+1: [np.random.uniform(-200, 1100), np.random.uniform(-1100, 500)] 
            for i in range(k)
    }
    return merkezler

#atama
def uzaklikhesabi(df, merkezler):
    for i in merkezler.keys():
        df['uzaklik_{}'.format(i)] = (np.sqrt((df['x'] - merkezler[i][0]) ** 2 + (df['y'] - merkezler[i][1]) ** 2 ))
#
def atamaislemi(df, merkezler):
    uzaklikhesabi(df,merkezler)
    centroid_distance_cols = ['uzaklik_{}'.format(i) for i in merkezler.keys()]
    df['enyakin'] = df.loc[:, centroid_distance_cols].idxmin(axis=1) #merkezlerden hangisine en yakın olduğu bulundu
    df['enyakin'] = df['enyakin'].map(lambda x: int(x.lstrip('uzaklik_')))#merkeze göre 1,2 veya 3 değeri atandı
   
    return df



def mean(veri):
    try:
        sonuc=sum(veri)/len(veri)
    except: #eğer küme elemanı hiç yoksa /0 tanımsızlığından kurtarmak için
        sonuc=0
    return sonuc


def median(x):
    x = sorted(x)
    listlength = len(x) 
    num = listlength//2
    if listlength%2==0:
        try:
            middlenum = (x[num]+x[num-1])/2
        except: #eğer küme elemanı hiç yoksa(length==0) dizin dışına çıkmayı engeller
            middlenum = 0 
    else:
        middlenum = x[num]
    return middlenum

def guncelleme(k,yontem):
    for i in merkezler.keys():
        merkezler[i][0] = median(df[df['enyakin'] == i]['x'])
        merkezler[i][1] = median(df[df['enyakin'] == i]['y'])
    return k


def hatabul(df):
  for i in merkezler.keys():
     toplam ={ i: sum( df[df['enyakin'] == i]['uzaklik_{}'.format(i)]) for i in merkezler.keys()}
  values=toplam.values()
  total=sum(values)
  return total

def cizdir(hatalar,renk):
    lists = sorted(hatalar.items()) 
    x, y = zip(*lists) 
    plt.ylabel('hataların kareleri toplamı')
    plt.xlabel('k sayısı')
    plt.plot(x, y,color=renk)
    


k=[2,3,5,10,15,20]
merkezhesaplamayontemi=[mean,median]

hatalarmean= dict()
hatalarmedian=dict()

for j in merkezhesaplamayontemi:
    for i in k:
        merkezler= merkezolustur(i)
        df = atamaislemi(df, merkezler)
        
        print(df.head())
        
        eski_merkezler = copy.deepcopy(merkezler)
        
        merkezler = guncelleme(merkezler,j)
        
        
        for i in eski_merkezler.keys():
            eski_x = eski_merkezler[i][0]
            eski_y = eski_merkezler[i][1]
            dx = (merkezler[i][0] - eski_merkezler[i][0])
            dy = (merkezler[i][1] - eski_merkezler[i][1])
        
        
        df = atamaislemi(df, merkezler)#güncellenen merkezli değerleri df ye atadık
        
        
        #güncelleme sonlanana kadar devam et
        while True:
            enyakin_merkezler = df['enyakin'].copy(deep=True)
            merkezler = guncelleme(merkezler,j)
            df = atamaislemi(df, merkezler)
            if enyakin_merkezler.equals(df['enyakin']):
                break
        hata=hatabul(df)
        print("hata")
        print(hata)
        
        if(j==mean):
            hatalarmean[i]=hata
        else:
            hatalarmedian[i]=hata
        
cizdir(hatalarmean,'r')
cizdir(hatalarmedian,'g')
plt.show()