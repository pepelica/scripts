from Bio import SeqIO
import xlrd
import xlsxwriter


def get_names_of_foulders():
    genomesFolder = 'D:/downloads/Study/laboratory/EloE/data/downloaded/merged_ncbi'
    input_excel = 'D:/downloads/Study/laboratory/Results/res_indx_refined.xlsx'
    output_exel = 'D:/downloads/Study/laboratory/Results/res_strains.xlsx'

    xlrd_book = xlrd.open_workbook(input_excel, on_demand=True)
    sheet = xlrd_book.sheet_by_index(0)

    workbook = xlsxwriter.Workbook(output_exel)
    worksheet = workbook.add_worksheet()

    genomes = [sheet.row_values(rownum) for rownum in range(sheet.nrows)] #значения исходной таблицы
    #сразу скопируем в новый файл
    row = 0
    for rec in genomes:
        col = 0
        for item in rec:
            worksheet.write(row, col, item)
            col += 1
        row += 1

    genomes.reverse()
    genomes.pop()
    genomes.reverse()

    strains_list = ['strain']
    for rowlist in genomes:
        if rowlist[0]=='':
            strains_list.append('-')
            continue
        organism_name_list = rowlist[1]
        organism_name = organism_name_list[0]+ ' ' + organism_name_list[1]

        genomeFolder = organism_name_list+ '   ' + rowlist[0]
        genome = organism_name_list + '.gbk'
        try:
            record = SeqIO.read(genomesFolder+'/'+genomeFolder+'/'+genome, 'genbank')
        except(FileNotFoundError):
            print(FileNotFoundError)
            continue
                
        definition = record.description

        print(definition)
        strains_list = find_strains(definition, strains_list)

    #вписываем штаммы
    row = 0
    for i in strains_list:
        worksheet.write(row, sheet.ncols , i)
        row += 1
    workbook.close()

def find_strains(definition, strains_list):
    #находим название штамма
    def_list = definition.split(' ')
    if def_list[2] == 'strain' or def_list[2] =='str.':
        strain = def_list[3]
    else: strain = def_list[2]
    strains_list.append(strain)
    return strains_list
   
    
get_names_of_foulders()
