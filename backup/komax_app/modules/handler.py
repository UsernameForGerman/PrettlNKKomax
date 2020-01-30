#module handle data frames
# -*- coding: utf-8 -*-

import pandas as pd
from komax_app.modules.ioputter import write_to_xlsx
from komax_app.modules import swap_up, get_index, swap_sides, line_to_right

column_names = ["Примечание", "№ п/п", "Маркировка", "Вид провода", "№ провода", "Сечение", "Цвет",
                "Длина, мм (± 3мм)", "Уплотнитель 1", "Длина трубки, L (мм) 1", "Длина трубки, L (мм) 2",
                "Частичное снятие 1", "Частичное снятие 2", "Наконечник 1", "Аппликатор 1", "Уплотнитель 2",
                "Наконечник 2", "Аппликатор 2", "Номер жгута", "Армировка 1 (Трубка ПВХ, Тр.Терм., изоляторы)",
                "Армировка 2 (Трубка ПВХ, Тр.Терм., изоляторы)"]

def value_in_row(df, row, value):
    rows, cols = df.shape
    row_temp = row
    for col in range(cols):
        if df[col][row_temp] == value:
            return True

    return False

def is_empty_column(df, *args):
    if args is None or df is None:
        return False
    for arg in args:
        for i in df.iloc[:, arg]:
            if type(i) is not None:
                return False
    return True

def add_pair_columns(df, terminals):
    rows, cols = df.shape
    to_pair = False

    h1, h2 = get_index(df, "Наконечник 1")[0], get_index(df, "Наконечник 2")[0]
    a1 = get_index(df, "Уплотнитель 1")[0]
    a2 = get_index(df, "Уплотнитель 2")[0]
    pulloff2 = get_index(df, "Частичное снятие 2")[0]
    number = get_index(df, "№ провода")[0]
    length = get_index(df, "Длина, мм (± 3мм)")[0]

    rows_to_change = []

    for row in range(rows):
        value = df.iloc[row, a2]
        if type(value) is str and ("спаривание" in value or 'cпаривание' in value):
            rows_to_change.append(row)

    swap_sides(df, rows_to_change)

    pair_was = False
    row = 1
    while row < rows:
        arm1 = df.iloc[row, a1]         # армировка 1
        ter1 = df.iloc[row, h1]         # terminal 1
        if to_pair:
            if not pair_was:
                col = df.shape[1]
                df[col] = None
                df.iloc[0, col] = "Длина, мм (± 3мм) 2"
                col = df.shape[1]
                df[col] = None
                df.iloc[0, col] = "Наконечник 3"
                col = df.shape[1]
                df[col] = None
                df.iloc[0, col] = "№ провода 2"
                col = df.shape[1]
                df[col] = None
                df.iloc[0, col] = "Частичное снятие 3"
                pair_was = True

            # if both of terminals not empty
            if df.iloc[row, h2] is not None and df.iloc[row - 1, h2] is not None and df.iloc[row, h2] != df.iloc[row - 1, h2]:
                second_to_delete = False
                first_to_delete = False
                if row != rows - 1 and df.iloc[row, h2] != df.iloc[row + 1, h2]:
                    second_to_delete = True
                if df.iloc[row - 1, h2] != df.iloc[row - 2, h2]:
                    first_to_delete = True
                if first_to_delete and not second_to_delete:
                    # delete first
                    df.iloc[row - 1, h2] = None
                else:
                    # delete second
                    df.iloc[row, h2] = None

            line_to_right(df, row - 1, length, h2, number, pulloff2)
            df = df.drop(index=row)
            df.index = pd.Index(range(df.shape[0]))
            row -= 1
            rows -= 1
            df.iloc[row, [a1, a2]] = None

            to_pair = False
        elif type(arm1) is str and ("спаривание" in arm1 or 'cпаривание' in arm1) and not to_pair and ter1 in terminals:
            to_pair = True
        elif type(arm1) is str and ("спаривание" in arm1 or 'cпаривание' in arm1) and ter1 not in terminals:
            df.iloc[row, a1] = None
            df.iloc[row, h1] = None

        row += 1

    return df

#TODO:ask Rishat about normalz
def make_normal(df):
    # delete rows

    rows, cols = df.shape

    #TODO : make another indexes finding
    wire_number_col = get_index(df, "№", "п/п")[0]
    number_col, number_row = get_index(df, "Длина", "(± 3мм)")
    square_col = get_index(df, "Сечение")[0]
    col_color = get_index(df, "Цвет")[0]
    conn_color1 = get_index(df, "Наконечник 1")[0]
    conn_color2 = get_index(df, "Наконечник 2")[0]
    armirovka_col1 = get_index(df, "Уплотнитель 1")[0]
    armirovka_col2 = get_index(df, "Уплотнитель 2")[0]
    pvc_tube_col1 = get_index(df, "Армировка 1 (Трубка ПВХ, Тр.Терм., изоляторы)")[0]
    pvc_tube_col2 = get_index(df, "Армировка 2 (Трубка ПВХ, Тр.Терм., изоляторы)")[0]

    try:
        text_col, row_main = get_index(df, "Наконечник 1")
    except TypeError:
        text_col, row_main = get_index(df, "Маркировка")

    for row in range(rows):
        # row to delete

        row_is_bad = False

        # Delete Длина > 20 мм

        type_of_df_number_col_row = type(df.iloc[row, number_col])
        value = df.iloc[row, number_col]
        number_col_row_bad = type_of_df_number_col_row is int and value <= 20 and value is not None
        number_col_row_empty = type_of_df_number_col_row is str and (value == "" or value == " ") or type(value) is None

        # delete if экран in value

        type_of_df_color_col_row = type(df.iloc[row, col_color])
        color_col_row_bad = type_of_df_color_col_row is str and "экран" in df.iloc[row, col_color]
        cabel_row = type(df.iloc[row, 0]) is str and "Кабель" in df.iloc[row, 0]

        #TODO: delete print(EMPTY)
        if number_col_row_bad or color_col_row_bad or number_col_row_empty or cabel_row:
            row_is_bad = True
        if number_col_row_empty:
            print("EMPTY")

        for col in range(cols):
            type_of_df_row_col = type(df.iloc[row, col])

            # Delete NaN values
            if df.iloc[row, col] != df.iloc[row, col]:
                df.iloc[row, col] = None

            # Delete Длина <= 20 мм
            if row_is_bad:
                df.iloc[row, col] = None

            # Delete статус rows
            if df.iloc[row, text_col] == "Статус" or df.iloc[row, text_col - 1] == "Статус" or df.iloc[row, text_col + 1] == "Статус":
                for col in range(cols):
                    df.iloc[row, col] = None
                    df.iloc[row + 1, col] = None

            if df.iloc[row, col_color] is None and df.iloc[row, square_col] is None:
                df.iloc[row, col] = None

            value = df.iloc[row, col]
            if type(value) is str and col != square_col and col != col_color and col != wire_number_col:
                if "R" in value:
                    df.iloc[row, col] = None


        value = df.iloc[row, square_col]
        if row != 0 and type(value) is str:
            df.iloc[row, square_col] = value.replace(',', '.')
            df.iloc[row, square_col] = float(df.iloc[row, square_col])

        """
        # delete "-" in armirovka
        value = df.iloc[row, armirovka_col1]
        value2 = df.iloc[row, armirovka_col2]
        if value == '-':
            df.iloc[row, armirovka_col1] = None
        if value2 == '-':
            df.iloc[row, armirovka_col2] = None
        """

        # delete CB in connectors
        conn1 = df.iloc[row, conn_color1]
        conn2 = df.iloc[row, conn_color2]
        if type(conn1) is str:
            if "СВ" in conn1 or "CB" in conn1:
                df.iloc[row, conn_color1] = None
        if type(conn2) is str:
            if "СВ" in conn2 or "CB" in conn2:
                df.iloc[row, conn_color2] = None

        # recognize color like 5 (K)
        if type(df.iloc[row, col_color]) is str and '(' in df.iloc[row, col_color]:
            index = 0
            try:
                index = df.iloc[row, col_color].index('(')
            except ValueError:
                pass
            color = df.iloc[row, col_color][index + 1]
            df.iloc[row, col_color] = color

        if df.iloc[row, pvc_tube_col1] is not None and row != 0 and not 'спаривание' in df.iloc[row, pvc_tube_col1]:
            df.iloc[row, pvc_tube_col1] = None
            df.iloc[row, conn_color1] = None
            df.iloc[row, armirovka_col1] = None
        if df.iloc[row, pvc_tube_col2] is not None and row != 0 and not 'спаривание' in df.iloc[row, pvc_tube_col2]:
            df.iloc[row, pvc_tube_col2] = None
            df.iloc[row, conn_color2] = None
            df.iloc[row, armirovka_col2] = None

    # check for the head(1)
    row_main = 0
    for col in range(cols):
        if df.iloc[row_main, col] not in column_names:
            for row in range(rows):
                df.iloc[row, col] = None

    df = df.dropna(how='all', axis=0)
    df = df.dropna(how='all', axis=1)

    df.columns = range(df.shape[1])
    df.index = pd.Index(range(df.shape[0]))

    rows, cols = df.shape
    for column_name in column_names:
        if get_index(df, column_name) == -1:
            data = {cols: [column_name] + [0 for i in range(rows)]}
            df2 = pd.DataFrame(data=data)
            df = df.join(df2)
            cols += 1

    pulloff_1 = get_index(df, "Частичное снятие 1")
    pulloff_2 = get_index(df, "Частичное снятие 2")

    while True:
        list = []
        rows, cols = df.shape
        for row in range(1, rows):
            for col in range(cols):
                value = df.iloc[row, col]
                if type(value) is str:
                    if 'Частичное снятие' in value:
                        list = [row, col]
        if not list:
            break

        if list[0] != 0:
            df.iloc[list[0], list[1]] = None
            name_of_column = df.iloc[0, list[1]]
            if type(name_of_column) is str:
                if '2' in name_of_column:
                    df.iloc[list[0], pulloff_2] = 16
                elif '1' in name_of_column:
                    df.iloc[list[0], pulloff_1] = 16

    return df

def df_array_to_df(array, print_xlsx=False, name='df_array_to_df_result'):
    print_xlsx = print_xlsx
    length_array = len(array)
    data = dict()

    for i in range(length_array):
        if print_xlsx:
            write_to_xlsx(array[i], name)
            print_xlsx = True

        rows, cols = array[i].shape
        list_names = []

        for col in range(cols):
            name = array[i].iloc[0, col]
            list_names.append(name)

            list_values = []

            for row in range(1, rows):
                list_values.append(array[i].iloc[row, col])

            if name in data:
                data[name] += list_values
            else:
                data[name] = list_values

    df = pd.DataFrame.from_dict(data)
    df = df.replace({pd.np.nan: None})

    temp_dict = dict()

    for col in df.columns:
        temp_dict[col] = col

    rows, cols = df.shape
    df = df.append(pd.DataFrame(data=temp_dict, index=pd.Index([rows])))

    swap_up(df, rows, 0)

    df.columns = range(cols)

    return df

def division_into_black_white_groups(df):
    black_df = pd.DataFrame()
    white_df = pd.DataFrame()

    mark_col = get_index(df, "Маркировка")[0]
    for index, row in df.iterrows():
        if index == 0:
            white_df = white_df.append(row, ignore_index=True)
            black_df = black_df.append(row, ignore_index=True)

        mark = df.iloc[index, mark_col]

        if type(mark) is str and "б" in mark.lower():
            white_df = white_df.append(row, ignore_index=True)
        elif type(mark) is str and "ч" in mark.lower() or mark != mark or mark is None or (type(mark) is str and mark == ''):
            black_df = black_df.append(row, ignore_index=True)


    return [white_df, black_df]

def get_df_sorted_by_komax(df, alloc):
    try:
        komax_col = get_index(df, "komax")[0]
    except TypeError:
        komax_col = -1

    if komax_col == -1:
        return komax_col

    rows, cols = df.shape
    df_dict = {}

    for key, item in alloc.items():
        if item[0] > 0:
            df_dict[key] = pd.DataFrame(df[0:][:1])

    for row in range(1, rows):
        komax_number = df.iloc[row, komax_col]
        if komax_number in df_dict:
            temp_df = df[0:][row:row + 1]
            df_dict[komax_number] = df_dict[komax_number].merge(temp_df, how='outer')
        else:
            pass

    return df_dict

def deleted_columns_with_name(df, name):
    while True:
        try:
            col, row = get_index(df, name)
        except:
            return df
        df = df.drop(columns=col)
        df.columns = range(df.shape[1])






