import os
from Bio import SeqIO

genomesFolder = 'D:\\downloads\\Study\\laboratory\\EloE\\data\\downloaded\\merged_ncbi'
genomes = os.listdir(genomesFolder)
for genomeFolder in genomes:
    contents = os.listdir(genomesFolder+'/'+genomeFolder)
    genome = contents[0]
    records = [rec for rec in SeqIO.parse(genomesFolder+'/'+genomeFolder+'/'+genome, 'genbank')]
    for rec in records:
        defin = rec.annotations['organism']
        acc = rec.annotations['accessions']
        break
    new_filename = defin.lower()+'.gbk'
    os.rename(genomesFolder+'\\'+genomeFolder+'\\'+genome, genomesFolder+'\\'+genomeFolder+'\\'+new_filename)
    os.rename(genomesFolder+'\\'+genomeFolder, genomesFolder+'\\'+defin.lower()+'   '+str(acc))
