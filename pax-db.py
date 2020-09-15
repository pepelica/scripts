import os
path = "D:\\downloads\\Study\\laboratory\\EloE\\data\\downloaded\\for_pax-db"
folder = os.listdir(path)
for i in folder:
    new_folder = str(i)[0:-3]
    os.makedirs(path+ '\\'+new_folder)
    print(os.getcwd)
    os.replace(path+'\\'+i, path+'\\'+new_folder+ '\\'+ i)