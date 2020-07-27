# -*- coding: utf-8 -*-

import random
from komax_app.modules.timer import time_changeover
from komax_app.modules import dict_column_numbers, swap_rows, get_index, count_unique, swap_sides, group_by

column_names = ["Примечание", "№ п/п", "Маркировка", "Вид провода", "№ провода", "Сечение", "Цвет",
                "Длина, мм (± 3мм)", "Уплотнитель 1", "Длина трубки, L (мм) 1", "Длина трубки, L (мм) 2",
                "Частичное снятие 1", "Частичное снятие 2", "Наконечник 1", "Апликатор 1", "Уплотнитель 2",
                "Наконечник 2", "Апликатор 2", "Номер жгута", "Армировка 1 (Трубка ПВХ, Тр.Терм., изоляторы)",
                "Армировка 2 (Трубка ПВХ, Тр.Терм., изоляторы)"]

time_square = 275   # Обучение - 150 сек,
time_wire = 70
time_connector = 435    # Обучение - 150 сек,
time_armirovka = 360

def bottom_group(df, row, col_ax):
    rows = df.shape[0]
    if row < rows - 1:
        if df[col_ax][row] != df[col_ax][row + 1]:
            return True
        return False
    elif row == rows - 1:
        if df[col_ax][row] != df[col_ax][row - 1]:
            return True
        return False
    return False

def quicksort(nums, col, fst, lst):
    if fst >= lst: return

    i, j = fst, lst
    pivot = nums[col][random.randint(fst, lst)]

    while i <= j:
        while nums[col][i] > pivot: i += 1
        while nums[col][j] < pivot: j -= 1
        if i <= j:
            swap_rows(nums, i, j)
            i, j = i + 1, j - 1
    quicksort(nums, col, fst, j)
    quicksort(nums, col, i, lst)

def quicksort_list(nums, fst, lst):
    if fst >= lst: return

    i, j = fst, lst
    pivot = nums[random.randint(fst, lst)]

    while i <= j:
        while nums[i] < pivot: i += 1
        while nums[j] > pivot: j -= 1
        if i <= j:
            nums[i], nums[j] = nums[j], nums[i]
            i, j = i + 1, j - 1
    quicksort(nums, fst, j)
    quicksort(nums, i, lst)

def find_element(element, df, column, start_from_index):
    rows = df.shape[0]

    if rows != start_from_index + 1:
        for row in range(start_from_index + 1, rows):
            if df[column][row] == element:
                return row
    return -1

def sort_groups(df, col_main, col_ax):
    rows = df.shape[0]

    for row in range(rows):
        if df[col_ax][row] is not None and row > 0:
            if bottom_group(df, row, col_ax):
                # find group_start element
                iter_row = row
                ax_element = df[col_ax][row]
                while df[col_ax][iter_row] == ax_element and iter_row > 0:
                    iter_row -= 1
                iter_row += 1
                # in quick sort row will be changed -> make copy
                copy_row = row
                quicksort(df, col_main, iter_row, copy_row)
            else:
                pass
        else:
            pass

def transfer_up_subgroup(df, row, col_ax, col_main):

    row_start_subgroup = row
    if row >= 1:
        if df[col_ax][row - 1] != df[col_ax][row] or row == df.shape[0] - 1:
            return
        else:
            pass
    else:
        return

    i = row

    while i >= 0:
        if df[col_ax][row] != df[col_ax][i]:
            i += 1
            break
        i -= 1

    #see transfer_group
    row_to_up = i
    row_end_subgroup = bottom_group(df, row, col_main)
    transfer_up_group(df, row_start_subgroup, row_end_subgroup, row_to_up)

def transfer_up_group(df, row_start_group, row_end_group, row_to_up):
    diff = row_start_group - row_to_up
    i = 1
    for row in range(row_start_group, row_end_group + 1):
        if (i > diff):
            break
        tmp_row = row
        while tmp_row > (row_to_up + i):
            swap_rows(df, tmp_row, tmp_row - 1)
            tmp_row -= 1
        i += 1

def smart_sort(df, col_main, col_ax):
    rows = df.shape[0]
    row = 1

    while row < rows:
        if type(df.iloc[row, col_main]) is not None and type(df.iloc[row, col_ax]) is not None:
            if bottom_group(df, row, col_ax):
                element_row = find_element(df[col_main][row], df, col_main, row)
                if (element_row != -1):
                    copy_row = element_row
                    transfer_up_subgroup(df, copy_row, col_ax, col_main)
                    row_end_group = element_row
                    while not bottom_group(df, row_end_group, col_ax) and row_end_group < rows - 1:
                        row_end_group += 1

                    transfer_up_group(df, element_row, row_end_group, row)
                row += 1
            else:
                row += 1
        else:
            row += 1

def fulfill_row_none(df, row):
    cols = df.shape[1]
    i = 0
    for col in df.columns:
        if i < cols:
            df[col][row] = None
        else:
            break
        i += 1

def values_in_row(df, row):
    cols = df.shape[1]
    cnt = 0

    for col in range(cols):
        if not df[col][row] is None:
            cnt += 1

def to_str_type_column(df, col):
    r = df.shape[0]

    for i in range(r):
        if type(df[col][i]) is int or type(df[col][i]) is float:
            df[col][i] = str(df[col][i])
        elif df[col][i] is None:
            df[col][i] = ''
        elif type(df[col][i]) is str:
            pass

def row_contain_word(df, row, word):
    cols = df.shape[1]

    for i in range(cols):
        if df[i][row] != None and type(df[i][row]) is str and word == df[i][row]:
            return True

    return False

def row_is_empty(df, row):
    cols = df.shape[1]

    for col in range(cols):
        if df[col][row] != None:
            return False
    return True

def value_in_row(df, row, value):
    rows, cols = df.shape
    row_temp = row
    for col in range(cols):
        if df[col][row_temp] == value:
            return True

    return False

def number_of_changeover_in_row(df, col):
    cnt = 0
    rows = df.shape[0]

    tmp = df.iloc[1, col]


    for row in range(1, rows):
        if tmp != df.iloc[row, col]:
            cnt += 1
            tmp = df.iloc[row, col]

    return cnt

def cols_to_list(df, *cols):
    output = []
    time = 0
    for col in cols:
        len_col = len(col)
        for i in range(1, len_col):
            if time == 0:
                output.append('')
            output[i - 1] += col[i]
            output[i - 1] += '|'
        time += 1
    rows, column = df.shape
    df[column] = 'list_for_sort'

    for row in range(1, rows):
        df.iloc[row, column] = output[row - 1]

    return

def dict_of_elements(df, row, element):
    rows, cols = df.shape
    out_dict = dict()

    for col in range(cols):
        if element in df.iloc[0, col]:
            out_dict[df.iloc[0, col]] = df.iloc[row, col]

    return out_dict

def swap_cols_if(df, col1, col2):
    rows, cols = df.shape
    element = 0
    row = 0
    stop = False

    # element finding

    while True:
        row_copy = row
        quicksort(df, col1, row_copy, rows - 1)
        while element == df.iloc[row, col1]:
            row += 1
            if row == rows:
                stop = True
                row -= 1
                break
        element = df.iloc[row, col1]
        if stop:
            break
        for i in range(row, rows):
            if df.iloc[i, col1] != element and df.iloc[i, col2] == element:
                tmp_row = 0
                for col in range(cols):
                    if type(df.iloc[tmp_row, col]) is str and '1' in df.iloc[tmp_row, col]:
                        column_one = col
                        column_two = get_index(df, df.iloc[tmp_row, col][0:-1] + '2')[0]
                        df.iloc[i, [column_one, column_two]] = df.iloc[i, [column_two, column_one]].values

def filter_for_equals(df, col1, col2, pairing=False):
    filtered = []
    rows, cols = df.shape
    rows_to_swap = []

    h3 = -1
    if pairing:
        try:
            h3 = get_index(df, "Наконечник 3")[0]
        except:
            h3 = -1

    for row in range(rows):
        if pairing and h3 != -1:
            if df.iloc[row, h3] is not None:
                filtered.append(df.iloc[row, col1])
        if df.iloc[row, col1] not in filtered:
            main_word = df.iloc[row, col1]
            if main_word != '':
                for i in range(rows):
                    left_word = df.iloc[i, col1]
                    right_word = df.iloc[i, col2]
                    if right_word == main_word and right_word != left_word and left_word not in filtered:
                        rows_to_swap.append(row)
                filtered.append(main_word)
    swap_sides(df, rows_to_swap)
    return df

def cols_to_filter(df):
    col_apl_1 = get_index(df, "Наконечник 1")[0]
    col_apl_2 = get_index(df, "Наконечник 2")[0]
    col1, col2 = col_apl_1, col_apl_2

    first_better_to_sort = count_unique(df, col1) >= count_unique(df, col2)

    if first_better_to_sort:
        return [col1, col2]
    else:
        return [col2, col1]

def sort_groups(df, groups_col, *other_cols):
    for col in other_cols:
        to_str_type_column(df, col)

    to_str_type_column(df, groups_col)
    other_cols_df = [df[col] for col in other_cols]
    cols_to_list(df, *other_cols_df)

    # first group : S<=1
    # second group : 1<S<=2.5
    # third group : > 2.5

    rows, cols = df.shape

    groups = {}

    for row in range(1, rows):
        square = float(df.iloc[row, groups_col])

        group = group_by(square)
        if group == 1 and 1 not in groups:
            groups[1] = [row]
        elif group == 2 and 2 not in groups:
            groups[2] = [row]
        elif group == 3 and 3 not in groups:
            groups[3] = [row]

        next_group = 0
        if row != rows - 1:
            next_square = float(df.iloc[row + 1, groups_col])
            next_group = group_by(next_square)
        else:
            next_group = -1

        if 1 in groups and (next_group == -1 or next_group != 1) and group == 1:
            groups[1].append(row)
        elif 2 in groups and (next_group == -1 or next_group != 2) and group == 2:
            groups[2].append(row)
        elif 3 in groups and (next_group == -1 or next_group != 3) and group == 3:
            groups[3].append(row)

    for key, item in groups.items():
        row_start = item[0]
        row_end = item[1]
        quicksort(df, cols - 1, row_start, row_end)

def make_sort_the_second(df, time, print_time=False):

    rows, cols = df.shape
    col_square, row_main = get_index(df, "Сечение")

    sort_times = []
    number_cols = dict_column_numbers(df)

    # 1 - square and color sort

    time_spend = 0

    col1 = col_square
    col2, col3 = cols_to_filter(df)

    to_str_type_column(df, col1)
    to_str_type_column(df, col2)
    to_str_type_column(df, col3)

    cols_to_list(df, df[col1], df[col2], df[col3])
    quicksort(df, cols, row_main + 1, rows - 1)

    sort_groups(df, col1, col2, col3)

    for row in range(1, rows):
        time_spend += time_changeover(df, row, number_cols, time)

    if print_time:
        print(time_spend)

    return df
