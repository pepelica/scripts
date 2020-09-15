# -*- coding: utf-8 -*-
"""
Created on Mon Jun  10 17:35:22 2019
2019.10.06

@author: yasana
"""

import pandas as pd
import os
import sys
from Bio import SeqIO

#Дешифровка выходной таблицы EloE: вычисляем по ней, входным данным и 
#названиям выходных папок, какие аксешены соответствуют строкам выходной
#таблицы EloE
#genomesFolder - путь до папки с входными геномами
#genomesFolder - путь до папки с результатами EloE
def decryptEloEoutput(genomesFolder, eloeResFolder):
    #Считываем выходную таблицу EloE
    dfEloEtable = pd.read_csv(eloeResFolder+"/organisms_index.txt", delimiter='\t')
    #добавляем ещё одну колонку для генбанковских айдишников
    newCols = dfEloEtable.columns.insert(0,'GENBANK')
    dfEloEtable = dfEloEtable.reindex(columns = newCols)
    dfEloEtable['GENBANK'] = dfEloEtable['GENBANK'].astype('object')#костыль, чтоб не валилось с ValueError
    genomes = os.listdir(genomesFolder)
    #Запускаем цикл по входным геномам: для каждого генома находим все строки
    for genomeFolder in genomes:# в таблице EloE, имеющие тот же род-вид
         contents = os.listdir(genomesFolder+'/'+genomeFolder)
         if len(contents)<1:
             continue#пустые папки не трогаем
         #взяли геном за рога и вытаскиваем всё, что нужно из него
         tmp = genomeFolder.split(' ')
         if len(tmp)<1:
             print("Warning! No NCBI accession is found for " + genomeFolder + ". Skipping it...")
             continue
         #по построению названий этих входных папок с геномами там
         acc = tmp[-1]#последним идёт GENBANK ID
         if acc=='':
             print("Warning! No NCBI accession is found for " + genomeFolder + ". Skipping it...")
             continue
         acc=acc.split('.')[0]#удаляем версию accession (через точку)
         genome = contents[0]#там всего один файл лежит в этой папке по построению
         rec = SeqIO.read(genomesFolder+'/'+genomeFolder+'/'+genome, 'genbank')
         torg = rec.annotations['organism']
         #acc = rec.annotations['accessions']
         tmp1 = torg.split(' ')
         if len(tmp1)<2:
             print("Warning! The genus-species info is missing for " + genomeFolder + ". Skipping it...")
             continue
         genus = tmp1[0].lower()
         org = genus + ' ' + tmp1[1].lower()#"genus species"
         #находим все строки в таблице EloE, имеющие тот же род-вид
         foundFlag = False
         dfOrg = dfEloEtable.loc[dfEloEtable['Organism'].str.startswith(org)]
         for index, row in dfOrg.iterrows():#перебираем полученную подтаблицу
             genlen = row['Genome length, bp']
             if rec.__len__() == int(genlen):#проверка, что длина генома совпадает
                 #Ура, мы нашли его! Добавляем аксешен
                 print("Found " + row['Organism'] + " EloE results for " + org)
                 dfEloEtable.at[index, 'GENBANK'] = acc
                 foundFlag = True
                 break
         #Если мы проделали всё это, но результат EloE так и не нашли, то поднимаемся до уровня рода 
         if False == foundFlag:
             dfOrg1 = dfEloEtable.loc[dfEloEtable['Organism'].str.startswith(genus)]
             for index, row in dfOrg1.iterrows():#перебираем полученную подтаблицу
                 genlen = row['Genome length, bp']
                 if rec.__len__() == int(genlen):#проверка, что длина генома совпадает
                     #Ура, мы нашли его! Добавляем аксешен. Но! Это может быть
                     #какой-то не тот вид, поэтому на всякий случай выводим пару
                     print("Warning! Ambigous species. Genbank accession: " + acc)
                     print("Found " + row['Organism'] + " EloE results for " + org)
                     dfEloEtable.at[index, 'GENBANK'] = acc
                     foundFlag = True
                     break
             if False == foundFlag:#так и не нашли - что ж поделаешь... вероятно, плазмида
                 print("No EloE results found for " + org + ". Genbank accession: " + acc)
    return dfEloEtable

DIR = 'D:\downloads\Study\laboratory'
eloeResFolder = DIR+'\Results\Results_ncbi'
genomesFolder = DIR+'\EloE\data\downloaded\merged_ncbi'

decDF = decryptEloEoutput(genomesFolder, eloeResFolder)
decDF.to_csv(path_or_buf = DIR+'/eloe_output_decrypted.tsv', sep="\t", index = False)#debug