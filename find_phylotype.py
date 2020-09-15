from Bio import SeqIO
import os
import pandas as pd
from pandas import ExcelWriter

def find_pylotype(genomeFolder):
    genomesFolder = 'D:\\downloads\\Study\\laboratory\\EloE\\data\\downloaded\\merged_ncbi'
    phylotype = []

    try:
        contents = os.listdir(genomesFolder+'/'+genomeFolder)           
    except(FileNotFoundError):
        return None 
        #читаем геномную карточку
    genome = contents[0]
    record = SeqIO.read(genomesFolder+'/'+genomeFolder+'/'+genome, 'genbank')
        #ищем в ней сигнальные последовательности филотпов
    if 'CGTTGATGAGGCGCGCAATTT' in record:
        phylotype.append('1')

    if 'AGTTATGGACGGTGGAAGTC' in record:
        phylotype.append('2')

    if 'ATTACGAGAGCAATCGAAAGATT' in record:
        phylotype.append('3')

    if 'ATTGCCAAGACGAGAGAAGTA' in record:
        phylotype.append('4')

        
    if len(phylotype)<1:
        phylotype.append(None)

    return phylotype

def main():
    phylotypes = []

    #открываем таблицу
    df = pd.read_excel(io = 'D:\\downloads\\Study\\laboratory\\Results\\res_strains.xlsx')

    #перебираем построчно
    for i in range (len(df)):
        genomeFolder = df.iloc[i]['Organism'] + '   ' + df.iloc[i]['GENBANK'] #содержимое двух ячеек - название папки с геномом этого организма
        print(genomeFolder)
        phylotypes.append(find_pylotype(genomeFolder)) #добавляем филотип этого организма в общий список филотипов

    #встраиваем этот список в качестве нового столбца
    df['Phylotypes'] = phylotypes

    
    #записываем в новый файл
    with ExcelWriter('D:\\downloads\\Study\\laboratory\\Results\\phylotypes.xlsx') as writer:
        df.to_excel(writer)

main()

    

