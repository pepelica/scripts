#ѕример, как можно работать с таблицей GOLD через pandas

import pandas as pd

DIR = 'D:/Dev/sokolov EloE/Data retrieval'

##„итаем данные из сводной таблицы
dfPivot = pd.read_excel(DIR+'/eloe_antismash_pivot_table_dbg.xlsx')
#вытаскиваем всЄ, что может быть нам интересно
df = pd.DataFrame(dfPivot, columns=['GENBANK', 'PHYLUM',
                                    'CLASS', 'ORDER', 'FAMILY',
                                    'GENUS', 'SPECIES', 'BGC type', 'Indx',
                                    'OXYGEN REQUIREMENT', 'METABOLISM', 'ENERGY SOURCES'#дополнительные пол€
                                    ])
taxLevel = 'GENUS'#'METABOLISM'#'ENERGY SOURCES'#выбираем таксономический уровень. “естировали на роде
#сортируем по роду
df = df.sort_values(by = taxLevel)
taxa = df[taxLevel].unique().tolist()
#далее можно посмотреть на сам датафрейм df и список taxa