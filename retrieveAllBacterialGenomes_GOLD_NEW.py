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
import os
import http
import json
#import sys
#import traceback

#скрипт для вытягивания геномов бактерий из NCBI на основе данных о собранных
#бактериальных геномах из GOLD
#UPD: слегка подправлен для распараллеливания процесса

#Задаём общие настройки
Entrez.email = 'klimenko@bionet.nsc.ru'
DIR = 'D:\downloads\Study\laboratory\EloE\data'

#Разбираемся с данными из GOLD
#dfOrganism = pd.read_excel(io = DIR+'/goldData-test.xlsx', sheet_name='Organism', usecols = ['ORGANISM NCBI GENUS', 'ORGANISM NCBI SPECIES'])
df = pd.read_excel(io = DIR+'/Ralstonia.xlsx', usecols = ['AP NAME','AP GENBANK'])

#df = pd.concat([dfOrganism, dfAnalysis], axis=1, join='inner')
#pd.concat([dfOrganism, dfAnalysis], axis=1).reindex(dfOrganism.index)
print(df)
#ldata = df.values.tolist()#развернули в список, чтоб удобней было дальше работвать
#Берём всё бактериальное, достаточно хорошее, что получило Genbank ID
#нет accession, нет разговора
#idx = df.index.values('Actinomadura')
#bact_genomes = df.loc[idx]

bad_list = []#список аксешенов, по которым ну никак не получается выкачать геном


#Делаем запросы в NCBI и записываем результат в файлы на диске
for row in df.itertuples():#перебираем полученную подтаблицу
    print(row)
    accessions = []
    species = row[1]
    ap_gbk_list = row[2]
    if ap_gbk_list == None: 
        print(species+"don't have an accession")
        continue
    appp = ap_gbk_list[1:-1]
    app = list(appp.split('},'))
    for i in app:
        try:
            ap = json.loads(i) 
        except(json.JSONDecodeError):
            try:
                i= i+'}'
                ap = json.loads(i) 
            except(json.JSONDecodeError):
                print(species+"_don't have an accession")
                continue
        accessions.append(ap.get('genbankId'))
    try:
        #Иногда слэши бывают в названиях вида...
        if species.find('/') > -1:
            species = species.replace('/', '[slash]')
        #А иногда - двоеточия...
        if species.find(':') > -1:
            species = species.replace(':', '[colon]')
    except(AttributeError):
        species = "NaN"
    #Перенесли эту проверку в условие индексирования выше
#    if pd.isnull(ac):#нет accession, нет разговора
#        continue
    
    #иногда в поле GENBANK много значений указывают на одну и ту же сборку,
    #поэтому делаем цикл по ним и выкачиваем все.

    for acc in accessions:
        acc = acc.strip()
        directory = DIR+'/downloaded/Ralstonia/'+species+' '+acc
        proj = species #getattr(row, 'PROJECT NAME')
        #if not os.path.exists(directory):#проверка нужна, чтобы не перезаписывать уже имеющиеся папки
        #проверка на основе значения accession, что ранее такого генома не скачивали
        ld1 = os.listdir(DIR+'/downloaded/')
        tmp1 = [x.split(' ')[-1] for x in ld1]#извлекли список аксешенов
        ac_list1 = [x.split('.')[0] for x in tmp1]#удалили версию, если таковая имелась
        ld2 = os.listdir(DIR+'/downloaded/Ralstonia/')
        #Проверяем ещё в одном месте
        tmp2 = [x.split(' ')[-1] for x in ld2]#извлекли список аксешенов
        ac_list2 = [x.split('.')[0] for x in tmp2]#удалили версию, если таковая имелась
        ac_list = ac_list1 + ac_list2#объединяем в единый список
        if not (acc in ac_list):#проверка нужна, чтобы не перезаписывать уже имеющиеся папки
            gotIt = False
            attempt = 1
            print("Start processing " + proj)
            print("Accession: " + acc)
            while (gotIt == False):
                try:
                    gb_acc = Entrez.efetch(db='nuccore', id=acc, rettype='gb', retmode='text')
                    gotIt = True
                    continue
                except urllib.error.HTTPError as herr:
                    print("Failed efetch: HTTPError %s. Making %s attempt..." % (herr.code, attempt))
    #                    print("Too much attempts. Terminate.")
    #                    sys.exit()
                except urllib.error.URLError as uerr:
                    print("Failed efetch. Reason %s. Making %s attempt..." % (uerr.reason, attempt))
                except (http.client.IncompleteRead):
                    print("Failed efetch. http.client.IncompleteRead. . Making %s attempt..." % attempt)
    #                    print("Too much attempts. Terminate.")
    #                    sys.exit()
                    #except (urllib.error.HTTPError, urllib.error.URLError) as e:
                    #traceback_str = ''.join(traceback.format_tb(e.__traceback__))
                #end try:
                #Сюда попадаем, только если сработало одно из исключений выше
                attempt += 1
                time.sleep(3)
                if attempt>4:
                    print("Too much attempts. Added to bad_list. Next")
                    bad_list.append(acc)
                    attempt=1
                    break
            #end while (gotIt == False):
            if (gotIt == True):
                for rec in SeqIO.parse(gb_acc, 'genbank'):
                    os.makedirs(directory)#дополнительные проверки не нужны, т.к. если сюда попали, значит такой директории нет
                    i = 1
                    SeqIO.write(rec, directory+'/'+species+'_'+str(i)+'.gbk', 'gb')
                    i =+ 1
                print(proj)
                time.sleep(3)
            else:
                print(proj + ' added to bad_list.')
        else:
            print(proj)#чтоб было видно, что мы прошли данную строчку

#записывам аксешены, которые выкачать не удалось
fw = open(DIR+'/bad_list.txt', 'w')
for line in bad_list:
    fw.write(line)
    fw.write('\n')
fw.close()