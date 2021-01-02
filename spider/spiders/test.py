df_rank = dict()
for i in range(1, 4):
    df_rank['ranks_' + str(i)] = {'_v1': 'return_1 >= 9',
                                  '_v2': 'return_1 >= 8 and return_1 < 9',
                                  '_v3': 'return_1 >= 7 and return_1 < 8',
                                  '_v4': 'return_1 >= 6 and return_1 < 7',
                                  '_v5': 'return_1 >= 7 and return_1 < 6',
                                  '_v6': 'return_1 >= 3 and return_1 < 5',
                                  '_v7': 'return_1 >= 0 and return_1 < 3',
                                  }

for rank_name, v in df_rank.items():
    print(rank_name)
    for rank_level, v in v.items():
        print(rank_level)
        print(v)