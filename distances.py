import numpy as np

# LAST COLLUMN IS UNLOADING DOCK
# LAST 2ND COLLUMN IS LOADING DOCK

four_machine_matrix = np.array([
        [0, 5, 10, 10, 6, 9],
        [5, 0, 10, 10, 6, 9],
        [10, 10, 0, 5, 11, 6],
        [10, 10, 5, 0, 11, 6],
        [6, 6, 11, 11, 0, 10],
        [9, 9, 6, 6, 10, 0]
    ])

empty_matrix = np.array([
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0]
])

sim_matrix = np.array([
    [0, 5.16, 10.258, 10.258, 6.12, 9.258],
    [5.16, 0, 10.258, 10.258, 6.12, 9.258],
    [10.258, 10.258, 0, 5.16, 11.218, 6.86],
    [10.258, 10.258, 5.16, 0, 11.218, 6.86],
    [6.12, 6.12, 11.218, 11.218, 0, 10.22],
    [9.258, 9.258, 6.86, 6.86, 10.22, 0]
])

six_machine_matrix = np.array([
    [0, 8, 12, 12, 16, 16, 9, 14],
    [8, 0, 12, 12, 16, 16, 9, 14],
    [12, 12, 0, 8, 12, 12, 13, 10],
    [12, 12, 8, 0, 12, 12, 13, 10],
    [16, 16, 12, 12, 0, 8, 17, 6],
    [16, 16, 12, 12, 8, 0, 17, 6],
    [9, 9, 13, 13, 17, 17 ,0, 15],
    [14, 14, 10, 10, 6, 6, 15, 0]
])

# LOADING DOCK FIRST
# six_machine_matrix = np.array([
#     [ 0,  9,  9, 13, 13, 17, 17, 15],
#     [ 9,  0,  8, 12, 12, 16, 16, 14],
#     [ 9,  8,  0, 12, 12, 16, 16, 14],
#     [13, 12, 12,  0,  8, 12, 12, 10],
#     [13, 12, 12,  8,  0, 12, 12, 10],
#     [17, 16, 16, 12, 12,  0,  8,  6],
#     [17, 16, 16, 12, 12,  8,  0,  6],
#     [15, 14, 14, 10, 10,  6, 6, 0]
# ])

five_machine_matrix = np.array([
    [0, 8, 12, 12, 16, 9, 14],
    [8, 0, 12, 12, 16, 9, 14],
    [12, 12, 0, 8, 12, 13, 10],
    [12, 12, 8, 0, 12, 13, 10],
    [16, 16, 12, 12, 0, 17, 6],
    [9, 9, 13, 13, 17, 0, 15],
    [14, 14, 10, 10, 6, 15, 0]
])


# LOADING DOCK FIRST
# five_machine_matrix = np.array([
#     [ 0,  9,  9, 13, 13, 17, 15],
#     [ 9,  0,  8, 12, 12, 16, 14],
#     [ 9,  8,  0, 12, 12, 16, 14],
#     [13, 12, 12,  0,  8, 12, 10],
#     [13, 12, 12,  8,  0, 12, 10],
#     [17, 16, 16, 12, 12,  0,  6],
#     [15, 14, 14, 10, 10,  6,  0]
# ])

ten_machine_matrix = np.array([
    [0, 10, 14, 18, 7, 12, 17, 37, 32, 27, 42, 20],
    [46, 0, 10, 14, 47, 8, 13, 33, 28, 23, 38, 16],
    [42, 46, 0, 10, 43, 48, 9, 29, 24, 19, 34, 12],
    [38, 42, 46, 0, 39, 44, 49, 25, 20, 15, 30, 8],
    [46, 9, 13, 17, 0, 11, 16, 36, 31, 26, 44, 19],
    [41, 45, 8, 12, 42, 0, 10, 31, 26, 21, 39, 14],
    [36, 40, 44, 7, 37, 42, 0, 26, 21, 16, 31, 9],
    [19, 23, 27, 31, 20, 25, 30, 0, 45, 40, 11, 33],
    [24, 28, 32, 36, 25, 30, 35, 11, 0, 45, 16, 38],
    [29, 33, 37, 41, 30, 35, 40, 16, 11, 0, 21, 43],
    [10, 14, 18, 22, 11, 16, 21, 40, 35, 30, 0, 24],
    [32, 36, 40, 44, 33, 38, 43, 19, 14, 9, 24, 0]
])

# LOADING DOCK FIRST
# ten_machine_matrix = np.array([
#     [ 0, 10, 14, 18, 22, 11, 16, 21, 40, 35, 30, 24],
#     [42,  0, 10, 14, 18, 7, 12, 17, 37, 32, 27, 20],
#     [38, 46, 0, 10, 14, 47, 8, 13, 33, 28, 23, 16],
#     [34, 42, 46, 0, 10, 43, 48, 9, 29, 24, 19, 12],
#     [30, 38, 42, 46, 0, 39, 44, 49, 25, 20, 15, 8],
#     [44, 46, 9, 13, 17, 0, 11, 16, 36, 31, 26, 19],
#     [39, 41, 45,  8, 12, 42,  0, 10, 31, 26, 21, 14],
#     [31, 36, 40, 44,  7, 37, 42,  0, 26, 21, 16, 9],
#     [11, 19, 23, 27, 31, 20, 25, 30,  0, 45, 40, 33],
#     [16, 24, 28, 32, 36, 25, 30, 35, 11,  0, 45, 36],
#     [21, 29, 33, 37, 41, 30, 35, 40, 16, 11,  0, 43],
#     [24, 32, 36, 40, 44, 33, 38, 43, 19, 14, 9,  0]
# ])

