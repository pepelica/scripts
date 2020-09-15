import os
from Bio import SeqIO

def decryptEloEoutput(genomesFolder, eloeResFolder):

    dfEloEtable = pd.read_csv(eloeResFolder+"/organisms_index.txt", delimiter='\t')
    #добавляем ещё одну колонку для генбанковских айдишников
    newCols = dfEloEtable.columns.insert(0,'GENBANK')
    dfEloEtable = dfEloEtable.reindex(columns = newCols)
    dfEloEtable['GENBANK'] = dfEloEtable['GENBANK'].astype('object') 
    
    genomes = os.listdir(genomesFoulder)
    for genome in genomes:
        genome.re