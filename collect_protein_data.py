import os
import pandas as pd
from pandas import ExcelWriter
from matplotlib import pyplot
from scipy.stats import spearmanr





def merge_data(path_paxdb, path_resultsEloE, organism, folderpaxdb_list):    
    EloEresults = os.listdir(path_resultsEloE + '\\' + organism)
    for EloE_file in EloEresults:
        if '_eei' in EloE_file:

            file_all = pd.read_csv(path_resultsEloE+'\\'+organism + '\\'+EloE_file, delimiter='\t')
            break
    
    
    final_data = pd.DataFrame(data = file_all, columns = ['#','##','locus_tag','protein_id','EEI'])
    
    #получаем номер таксона из папки EloE, чтобы можно было найти соответствующий результат pax_db
    file_name = organism.split('_')
    taxon = file_name[-1]
    path_organism_paxdb = path_paxdb + '\\'+taxon
    paxdb_files = os.listdir(path_organism_paxdb)
    paxlist = []
    for paxdb_file in paxdb_files:
        #читаем файл paxdb как df
      #  if len(paxdb_files) == 1 or 'integrated' in paxdb_file:
        with open(path_organism_paxdb+'\\' + paxdb_file, 'r') as pax_db:
            paxdb_df = pd.read_csv(path_organism_paxdb+'\\' + paxdb_file, skiprows=11, delimiter = '\t', usecols = ['string_external_id', 'abundance'], converters={'string_external_id': str, 'abundance': float})
            #paxdb_content = pd.read_csv(path_organism_paxdb+'\\' + paxdb_file, skiprows=11, delimiter = '\t')
            #paxdb_df = pd.DataFrame(data = paxdb_content, columns = ['string_external_id', 'abundance'])

        
        for k in range(len(paxdb_df)):
            string_external_id = paxdb_df.iloc[k]['string_external_id']
            protein = string_external_id.split('.')[-1]
            paxdb_df.at[k, 'string_external_id'] = protein
        print (paxdb_df)
        
        if '_' not in paxdb_df.iloc[2]['string_external_id'] and '_' or 'RS' in final_data.iloc[2]['locus_tag']:
            #for i in range (len(final_data)):
                # locus_tag = str(final_data.iloc[i]['locus_tag'])
                #new_locus_tag = locus_tag.replace('_', '')
                #final_data.iloc[i]['locus_tag'] = new_locus_tag
            final_data['locus_tag'] = final_data['locus_tag'].str.replace('_', '')
            final_data['locus_tag'] = final_data['locus_tag'].str.replace('RS', '')
            print('locus '+organism+' corrected')
        
        final_data.astype({'locus_tag':'str', 'protein_id':'str'}).dtypes
        paxdb_df.astype({'string_external_id':'str'}).dtypes

        try:
            final_data = pd.merge(final_data, paxdb_df, left_on = 'locus_tag', right_on='string_external_id', how = 'outer')
            print(final_data)
            paxlist.append(paxdb_file)
            paxlist.append(paxdb_file)

            final_data = final_data.drop('string_external_id', axis = 1)
            #final_data = final_data.rename({'abundance': str(paxdb_file)}, axis = 'columns')
        except(ValueError):
            continue
 
    #final_data.columns = pd.MultiIndex.from_tuples(zip(['EloE']*5+['abundance']*len(paxdb_files), final_data.columns))
    idx = pd.IndexSlice
    abundance = final_data[final_data.columns[-len(file_name):]]
    #abundance = pd.DataFrame(data = final_data.loc(axis = 1)[('abundance', idx[:])])
    med = abundance.median(axis = 1, skipna = True)
    #median = median.rename('median')
    med = pd.DataFrame(data = med, columns =['median']) #Теперь будет работать!
    print(med)
#    median.columns = pd.MultiIndex.from_frame(median, names = ('abundance', 'median'))
    final_data = pd.merge(final_data, med, how = 'outer', left_on = True)

    print(final_data)
    return final_data, paxdb_files


def corr_analysis(final_data):
    #abundance = pd.DataFrame(data = final_data, columns= ['EEI', 'abundance'])

    idx = pd.IndexSlice
    abundance = final_data.loc(axis = 1)[('EloE', 'EEI'), ('abunance', idx[:])]
    print(abundance)
    for_corr = abundance.dropna()
    corr = for_corr.corr(method = 'spearman')
    return corr

    
def complicate_corr(final_data, paxdb_files, organism):
    data1 = final_data.loc(axis = 1)['EloE', 'EEI']
    corr_res = pd.DataFrame(columns = ['file_name', 'correlation', 'p-value'], index = [organism]*len(paxdb_files))
    for i in paxdb_files:
        data2 = final_data.loc(axis = 1)[i]
        #pyplot.scatter(data1, data2)
        #pyplot.show()
        coef, p = spearmanr(data1, data2)
        corr_res.append({'file_name':i, 'correlation':coef, 'p-value':p}, ignore_index=True)

    
    print('Spearmans correlation coefficient: %.3f' % coef)
    # interpret the significance
    alpha = 0.05
    if p > alpha:
        print('Samples are uncorrelated (fail to reject H0) p=%.3f' % p)
    else:
        print('Samples are correlated (reject H0) p=%.3f' % p)
    



path_paxdb = 'D:\\downloads\\Study\\laboratory\\pax-db\\pax-db'
path_resultsEloE = 'D:\downloads\Study\laboratory\Results\Results_pax-db_chromosome_only'
path_results = 'D:\\downloads\\Study\\laboratory\\Results\\paxdb_EloE'

folderEloE_list = os.listdir(path_resultsEloE)
folderpaxdb_list = os.listdir(path_paxdb)
for organism in folderEloE_list:
    results, paxdb_files = merge_data(path_paxdb, path_resultsEloE, organism, folderpaxdb_list)
    corr = complicate_corr(results, paxdb_files, organism)
    
    with ExcelWriter(path_results + '\\' + organism + '.xlsx') as writer:
        results.to_excel(writer, sheet_name='table')
        #corr.to_excel(writer, sheet_name = 'corr')


def record_txt_file():
    with open(path_results +'\\all_corr.txt', 'a+') as corr_file:
        corr_cell =  corr.loc['EEI']['abundance']
        for_write = '\n'+ organism + '\t' + str(corr_cell)
        corr_file.write(for_write)


    
    
