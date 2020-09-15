import xlrd
import openpyxl

DIR = 'D:\downloads\Study\laboratory\Results'
xlrd_book = xlrd.open_workbook(DIR+'\EloE_decr.xlsx', on_demand=True)
 
sheet = xlrd_book.sheet_by_index(0) 
list_of_indexes = ['Indx_refined'] 
thres = 5
def fun(sheet):
    #считываем таблицу
    vals = [sheet.row_values(rownum) for rownum in range(sheet.nrows)]
    vals.reverse()
    head = vals.pop()
    vals.reverse()
    #вычленяем М и R значения
    for one_row in vals:
        m_list = [one_row[3], one_row[5], one_row[7], one_row[9], one_row[11]]
        r_list = [one_row[4], one_row[6], one_row[8], one_row[10], one_row[12]]
        maximum = max(m_list)


        big_m = []
        low_r = []
        low_r_indexes = []

    #ищем большие M
        for i in range(5):
            if maximum - m_list[i] <=thres:
                low_r.append(r_list[i])
                low_r_indexes.append(i)

     #оставляем из них только те, для которых Rmin
        to_remove = []
        
        for i in low_r_indexes:
            if r_list[i] != min(low_r):
                to_remove.append(i)

        for i in to_remove:
            low_r_indexes.remove(i)

    # если таких несколько, выбираем тот, у которого М больше    
        for i in low_r_indexes:
            big_m.append(m_list[i])

        final_index = low_r_indexes[big_m.index(max(big_m))] + 1             

        list_of_indexes.append(final_index)
        print(one_row[0])
    return head, list_of_indexes, vals

head, indexes, vals = fun(sheet)
xlrd_book.release_resources()


import xlsxwriter
workbook = xlsxwriter.Workbook(DIR+'/res_Indx_refined.xlsx')
worksheet = workbook.add_worksheet()

#копируем таблицу
def add_means(list_of_meanings, row):
    for rec in list_of_meanings:
        col = 0
        for item in rec:
            worksheet.write(row, col, item)
            col += 1
        row += 1

col, row = 0, 0

# вписываем заголовок
for item in head:
    worksheet.write(row, col, item)
    col += 1

add_means(vals, 1)

#вписываем новые значения
row = 0
for i in indexes:
    worksheet.write(row, len(head), i)
    row += 1


workbook.close()


