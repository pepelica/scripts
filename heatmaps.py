import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
# sphinx_gallery_thumbnail_number = 2


def create_heatmaps(df, filename):
    vegetables = ["solanacearum", "pseudosolanacearum", "syzygii", "insidiosa", "mannitolilytica", "pickettii", "?"]
    farmers = ["Index_1", "Index_2", "Index_3", "Index_4", "Index_5"]

    harvest = np.array(df)


    fig, ax = plt.subplots()
    im = ax.imshow(harvest)

    # We want to show all ticks...
    ax.set_xticks(np.arange(len(farmers)))
    ax.set_yticks(np.arange(len(vegetables)))
    # ... and label them with the respective list entries
    ax.set_xticklabels(farmers)
    ax.set_yticklabels(vegetables)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
            rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    for i in range(len(vegetables)):
        for j in range(len(farmers)):
            text = ax.text(j, i, harvest[i, j],
                        ha="center", va="center", color="w")

    ax.set_title("Количество образцов по индексу и филотипу \n Indx")
    fig.tight_layout()
    plt.show()
    plt.savefig('D:\\downloads\\Study\\laboratory\\Results\\' + filename + '.png')

def count_indexes(index, classification, for_heatmaps):
    classes = ["['1']", "['2']", "['3']", "['4']", 'insidiosa', 'mannitolilytica', 'pickettii', '[None]']
    for i in range(len(classes)):
        if classification == classes[i]:
            if index == 1:
                for_heatmaps[i][0] += 1
                continue
            elif index == 2:
                for_heatmaps[i][1] += 1
                continue
            elif index == 3:
                for_heatmaps[i][2] += 1
                continue
            elif index == 4:
                for_heatmaps[i][3] += 1
                continue
            elif index == 5:
                for_heatmaps[i][4] += 1
    return for_heatmaps

def main():

    df_indx_first = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
    df_new_index = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
    df = pd.read_excel(io = 'D:\\downloads\\Study\\laboratory\\Results\\phylotypes.xlsx')
    for i in range (len(df)):
        index_first = df.iloc[i]['Indx']
        new_index = df.iloc[i]['Indx_refined']
        classification = df.iloc[i]['Phylotypes']
        df_indx_first = count_indexes(index_first, classification, df_indx_first)
        
        df_new_index = count_indexes(new_index, classification, df_new_index)
    print('df_indx_first', df_indx_first)
    print('df_new_index', df_new_index)
#   df_indx_first = [[0, 3, 3, 0, 21], [0, 10, 1, 0, 88], [0, 1, 0, 0, 12], [0, 0, 0, 4, 0], [0, 0, 0, 6, 1], [0, 0, 0, 14, 1], [0, 5, 3, 15, 19]]
#   df_new_index = [[0, 0, 0, 0, 27], [0, 4, 0, 0, 95], [0, 0, 0, 0, 13], [0, 0, 0, 4, 0], [0, 0, 0, 6, 1], [0, 0, 0, 13, 2], [0, 1, 2, 14, 25]]
    create_heatmaps(df_indx_first, 'EloE_index') #
    create_heatmaps(df_new_index, 'new_index')

main()




