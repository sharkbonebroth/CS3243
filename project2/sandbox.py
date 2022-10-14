arr_1 = [[False for i in range(10)] for j in range(10)]
arr_2 = [[True for i in range(10)] for j in range(10)]

arr_3 = [[arr_1[i][j] or arr_2[i][j] for j in range(10)] for i in range(10)]

print(arr_3)
print(sum(map(sum, arr_3)))