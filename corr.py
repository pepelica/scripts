import pandas as pd

path = 'D:\\downloads\\Study\\laboratory\\Results\\paxdb_EloE\\Bacteroides_thetaiotaomicron_VPI-5482_226186.xlsx'
import pandas as pd

colors = {'first_set':  ['Green','Green','Green','Blue','Blue','Red','Red','Red'],
          'second_set': ['Yellow','Yellow','Yellow','White','White','Blue','Blue','Blue']
         }

df = pd.DataFrame(colors, columns= ['first_set','second_set'])
df['first_set'] = df['first_set'].replace(['Blue','Red'],'Green')

print (df)
#df = pd.read_excel(path, header = [0,1])

#ряд табличек для корр. анализа

