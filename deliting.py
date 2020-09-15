import os
import shutil
from Bio import SeqIO

genomesFolder = 'D:\\downloads\\Study\\laboratory\\EloE\\data\\downloaded\\genome_assemblies_genome_gb (1)\\ncbi-genomes-2020-08-07' 

genomes = os.listdir(genomesFolder)

def check_CDS(path):
     records = [rec for rec in SeqIO.parse(path, 'genbank')]
     good_file = False
     for rec in records:
          if len(rec.features) > 10:
               good_file = True
     return good_file




for genomeFolder in genomes:# в таблице EloE, имеющие тот же род-вид
     contents = os.listdir(genomesFolder+'/'+genomeFolder)
     try: 
          genome = contents[0]#там всего один файл лежит в этой папке по построению
     except(IndexError):
          shutil.move(genomesFolder+'/'+genomeFolder, 'D:\\downloads\\Study\\laboratory\\EloE\\data\\downloaded\\bad_data')
          sum += 1
          continue
     path = genomesFolder+'/'+genomeFolder+'/'+genome
     #path = "D:\downloads\Study\laboratory\EloE\data\downloaded\genome_assemblies_genome_gb (1)\ncbi-genomes-2020-08-07\Ralstonia pickettii   ['CABKQE010000001', 'CABKQE010000000']\Ralstonia pickettii.gbk"
     size = os.path.getsize(path)
     print(genome, size)
     if size < 50000 or check_CDS(path) == False:
          try:
               shutil.move(genomesFolder+'/'+genomeFolder, 'D:\\downloads\\Study\\laboratory\\EloE\\data\\downloaded\\bad_data')
          except(shutil.Error):
               shutil.rmtree(genomesFolder+'/'+genomeFolder)
     
#     open_file = open(genomesFolder+'/'+genomeFolder+'/'+genome, 'r')
 #    rec = open_file.read()
  #   index = rec.find('translation')
  #   open_file.close()
  #   if index == -1:
  #        
  #   open_file.close()
     print(genomeFolder, genome)
