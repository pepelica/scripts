# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 14:21:44 2018

@author: yasana
"""

from Bio import SeqIO
from Bio import Entrez
import pandas as pd
import time
import urllib
#from itertools import chain
import os
import numpy as np

#скрипт для вытягивания геномов бактерий из NCBI

#Задаём общие насройки
Entrez.email = '<твой_имэйл>'
DIR = 'D:\downloads\Учебка\вероятно,диплом\EloE'

#Разбираемся с данными из Antismash-DB
dfAntismashDB = pd.read_excel(DIR+'\gold_complete_and_published_bacterial_genomes.xlsx')
df = pd.DataFrame(dfAntismashDB, columns=['NCBI BIOSAMPLE ACCESSION', 'GENUS', 'SPECIES'])
ldata = df.values.tolist()#развернули в список, чтоб удобней было дальше работвать


##accessions = list(chain(*accessions))#избавились от ненужной вложенности
#перебираем данные из таблицы, составляя словарь acc - геном вида
organismDict = dict()
for row in ldata:
    organismDict[row[0]] = str(row[1]) + ' ' + str(row[2]) + ' ' + str(row[0])
#выделяем уникальные геномы
accessions = df['NCBI BIOSAMPLE ACCESSION'].tolist()
acc_set = set(accessions)#множество уникальных идентификаторов геномов
#Делаем запросы в NCBI и записываем результат в файлы на диске
for acc in acc_set:
    directory = DIR+'\\output\\'+organismDict[acc]
    if acc is np.nan:
        continue
    else:
        if not os.path.exists(directory):#проверка нужна, чтобы не перезаписывать уже имеющиеся папки
            gotIt = False
            print("Start processing " + organismDict[acc])
            while (gotIt == False):
                try:
                    gb_acc = Entrez.efetch(db='nuccore', id=acc, rettype='gb', retmode='text')
                    gotIt = True
                except (urllib.error.HTTPError, urllib.error.URLError):
                    time.sleep(3)
            rec = SeqIO.read(gb_acc, 'genbank')
            os.makedirs(directory)#дополнительные проверки не нужны, т.к. если сюда попали, значит такой директории нет
            SeqIO.write(rec, directory+'\\'+organismDict[acc]+'.gbk', 'gb')
            print(organismDict[acc])
            time.sleep(3)
        else:
            print(acc)#чтоб было видно, что мы прошли данный идентификатор
    break
    

#print(dfAntismashDB['NCBI accession', 'From', 'To'])
#df.loc[df['column_name'] == some_value]

#acc = 'AE006468.2'
#start = 625464
#stop = 679053
#gb_acc2 = Entrez.efetch(db='nuccore', id=acc, rettype='gb', retmode='text', seq_start=start, seq_stop=stop)
#rec = SeqIO.read(gb_acc2, 'genbank')
#SeqIO.write(rec, 'bgc.gb.txt', 'gb')