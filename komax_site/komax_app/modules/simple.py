# this simple module makes simple operations with everything
# -*- coding: utf-8 -*-

def group_by(square):
    first_group = False
    second_group = False
    third_group = False

    if square <= 1.0:
        first_group = True
    elif 1.0 < square <= 2.5:
        second_group = True
    elif square > 2.5:
        third_group = True

    if first_group:
        return 1
    elif second_group:
        return 2
    elif third_group:
        return 3

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

def swap(a, b):
    tmp = b
    b = a
    a = tmp

def dict_column_numbers(df):
    rows, cols = df.shape
    number_cols = dict()

    for col in range(cols):
        value = df.iloc[0, col]
        if value == "Цвет":
            number_cols["Цвет"] = col
        elif value == "Сечение":
            number_cols["Сечение"] = col
        elif value == "Наконечник 1":
            number_cols["Наконечник 1"] = col
        elif value == "Наконечник 2":
            number_cols["Наконечник 2"] = col
        elif value == "Уплотнитель 1":
            number_cols["Уплотнитель 1"] = col
        elif value == "Уплотнитель 2":
            number_cols["Уплотнитель 2"] = col

    return number_cols

def swap_rows(df, row1, row2):
    b, c = df.iloc[row1].copy(), df.iloc[row2].copy()
    df.iloc[row1], df.iloc[row2] = c, b

def contain_letter(strg):
    if strg is not None:
        for symbol in strg:
            if (symbol >= 'а' and symbol <= 'я') or (symbol >= 'А' and symbol <= 'Я'):
                return True
    return False

def contain_word_in(string, *args):
    if args is None or string is None:
        return False
    for list in args:
        for word in list:
            if word is None:
                return False

            if type(word) is str and type(string) is str:
                if word in string:
                    continue
                else:
                    return False
            elif type(word) is int and type(string) is int:
                if word == string:
                    continue
                else:
                    return False
            else:
                return False

    return True

def get_index(data_frame, *args):
    rows, cols = data_frame.shape

    for i in range(cols):
        for index, rows in data_frame.iterrows():
            if not data_frame[i][index] is None:
                if contain_word_in(data_frame[i][index], args):
                    return [i, index]

    return -1

def swap_down(df, row, row_end):
    while row < row_end:
        swap_rows(df, row, row + 1)
        row += 1

def swap_up(df, row, row_up):
    while row > row_up:
        swap_rows(df, row, row - 1)
        row -= 1

def count_unique(data, column):
    return data.nunique()[column]

def is_empty(df):
    return False if df.shape[0] > 1 else True

def swap_sides(df, rows):
    h1, h2 = get_index(df, "Наконечник 1")[0], get_index(df, "Наконечник 2")[0]
    a1, a2 = get_index(df, "Уплотнитель 1")[0], get_index(df, "Уплотнитель 2")[0]
    length1, length2 = get_index(df, "Длина трубки, L (мм) 1")[0], get_index(df, "Длина трубки, L (мм) 2")[0]
    pulloff1, pulloff2 = get_index(df, "Частичное снятие 1")[0], get_index(df, "Частичное снятие 2")[0]
    pvc_tube1, pvc_tube2 = get_index(df, "Армировка 1 (Трубка ПВХ, Тр.Терм., изоляторы)")[0], get_index(df, "Армировка 2 (Трубка ПВХ, Тр.Терм., изоляторы)")[0]

    for row in rows:
        df.iloc[row, h1], df.iloc[row, h2] = df.iloc[row, h2], df.iloc[row, h1]
        df.iloc[row, a1], df.iloc[row, a2] = df.iloc[row, a2], df.iloc[row, a1]
        df.iloc[row, length1], df.iloc[row, length2] = df.iloc[row, length2], df.iloc[row, length1]
        df.iloc[row, pulloff1], df.iloc[row, pulloff2] = df.iloc[row, pulloff2], df.iloc[row, pulloff1]
        df.iloc[row, pvc_tube1], df.iloc[row, pvc_tube2] = df.iloc[row, pvc_tube2], df.iloc[row, pvc_tube1]

def line_to_right(df, row, *columns):
    # remember to drop row, which was moved to right

    rows, cols = df.shape

    cnt = len(columns)

    for column in columns:
        df.iloc[row, cols - cnt] = df.iloc[row + 1, column]
        cnt -= 1




