# module that gives time, allocation and etc
# -*- coding: utf-8 -*-

from komax_app.modules.ioputter import write_to_xlsx
from komax_app.modules import dict_column_numbers, get_index

def time_changeover(df, row, number_cols, time, volume=1, pairing=False):

    rows, cols = df.shape

    color_col = number_cols["Цвет"]
    square_col = number_cols["Сечение"]
    conn_col1 = number_cols["Наконечник 1"]
    conn_col2 = number_cols["Наконечник 2"]
    armirovka_col1 = number_cols["Уплотнитель 1"]
    armirovka_col2 = number_cols["Уплотнитель 2"]

    square_change, color_change, conn1_change, conn2_change = False, False, False, False
    armirovka1_change, armirovka2_change = False, False
    time_position = 0
    if not pairing:
        for col in range(cols):
            value = df.iloc[row, col]
            back_value = df.iloc[row - 1, col]

            if value != back_value:
                if col == color_col:
                    color_change = True
                elif col == square_col:
                    square_change = True
                elif col == conn_col1 and value != None and value != '':
                    conn1_change = True
                elif col == conn_col2 and value != None and value != '':
                    conn2_change = True
                elif col == armirovka_col1 and value != None and value != '':
                    armirovka1_change = True
                elif col == armirovka_col2 and value != None and value != '':

                    armirovka2_change = True
        if square_change:
            if conn1_change and conn2_change:
                time_position += (time['learn'] * 3 + time['aplicator'] * 2 + time['direction'] + time['contact'])
            elif not conn1_change and not conn2_change:
                time_position += (time['learn'] + time['direction'])
            else:
                time_position += (time['learn'] * 2 + time['aplicator'] + time['direction'] + time['contact'])
        else:
            if conn1_change and conn2_change:
                time_position += (time['learn'] * 2 + time['aplicator'] * 2 + time['contact'] * 2)
            elif not conn1_change and not conn2_change:
                pass
            else:
                time_position += (time['learn'] + time['aplicator'] + time['contact'])

        if square_change or color_change:
            time_position += time['wire']

        if armirovka1_change:
            time_position += time['compact']
        if armirovka2_change:
            time_position += time['compact']

        if time_position != 0:
            time_position += (time['pack'] + time['ticket'] + time['task'])

        time_position += volume * time['cut']
    else:
        time_position = time['aplicator']
    return time_position

def task_allocation(df, komaxes, quantity, time, hours):

    try:
        length2 = get_index(df, "Длина, мм (± 3мм) 2")[0]
    except TypeError:
        length2 = -1

    amount_of_komax = len(komaxes)

    # create dict of allocation
    alloc = {i: [0] for i in range(1, amount_of_komax + 1)}

    worker_time = hours*60*60       # in seconds

    rows, cols = df.shape

    column_numbers = dict_column_numbers(df)

    # get info of komaxes

    black_pairing_komax = 0
    white_pairing_komax = 0
    black_komax = 0
    white_komax = 0

    for key, item in komaxes.items():
        if komaxes[key][0] == 1:
            if komaxes[key][1] == 1:
                if komaxes[key][2] == 1 and white_pairing_komax == 0:
                    white_pairing_komax = key
                elif komaxes[key][2] == 0 and white_komax == 0:
                    white_komax = key
            elif komaxes[key][1] == 2:
                if komaxes[key][2] == 1 and black_pairing_komax == 0:
                    black_pairing_komax = key
                elif komaxes[key][2] == 0 and black_komax == 0:
                    black_komax = key

    if black_komax == 0:
        black_komax = black_pairing_komax
    if white_komax == 0:
        white_komax = white_pairing_komax

    amount_black_pairing_komax = 0
    amount_white_pairing_komax = 0

    amount_black_komax = 0
    amount_white_komax = 0

    for key, item in komaxes.items():
        if item[0] == 1 and item[1] == 1 and item[2] == 1:
            amount_white_pairing_komax += 1
        elif item[0] == 1 and item[1] == 2 and item[2] == 1:
            amount_black_pairing_komax += 1
        elif item[0] == 1 and item[1] == 1 and item[2] == 0:
            amount_white_komax += 1
        elif item[0] == 1 and item[1] == 2 and item[2] == 0:
            amount_black_komax += 1

    black_pairing_komax_more = amount_black_pairing_komax >= amount_white_pairing_komax
    black_komax_more = amount_black_komax >= amount_white_komax

    # get harness number and marking column

    harness_number_col = get_index(df, "Номер жгута")[0]
    mark_col = get_index(df, "Маркировка")[0]

    # adding columns with harnesses amount and komax number alloc

    df[cols] = None
    df.iloc[0, cols] = 'Amount'
    df[cols + 1] = None
    df.iloc[0, cols + 1] = 'komax'

    rows, cols = df.shape

    #count time for paired positions

    if length2 == -1:
        pass
    else:
        time_spend_black_pairing = 0
        time_spend_white_pairing = 0

        no_more_black_pairing = False
        no_more_white_pairing = False

        for row in range(1, rows):
            value = df.iloc[row, length2]
            quantity_harness = 0
            time_position = 0
            if value is None:
                pass
            else:
                harness = df.ix[row, harness_number_col]
                # quantity_harness = 1
                try:
                    quantity_harness = quantity[harness]
                except KeyError:
                    text_warn_rus_1 = "Проверь номера жгутов в файле кол-ва жгутов."
                    text_warn_rus_2 = "Не найден жгут номер {}".format(harness)
                    write_to_xlsx("Ошибка", "Выход/", text_warn_rus_1 + text_warn_rus_2)
                    raise KeyError("Check if harness number is correct in \"Количество.xlsx\" file! : {}".format(harness))

                time_position = time_changeover(df, row, column_numbers, time, volume=quantity_harness, pairing=True)

                df.iloc[row, cols - 2] = quantity_harness

                marking = df.iloc[row, mark_col]
                if type(marking) is str and 'б' in marking.lower():
                    if not no_more_white_pairing:
                        time_spend_white_pairing += time_position
                        if white_pairing_komax == 0:
                            text_warn_rus_1 = "Нет комаксов с белой маркировкой и возможностью спарки!"
                            write_to_xlsx("Ошибка", "Выход/", text_warn_rus_1)
                            raise Warning("No komaxes with white marking and pairing ability")
                        df.iloc[row, cols - 1] = white_pairing_komax
                    else:
                        #TODO: replace "спарки" with "спаривание" everywhere please!
                        text_warn_rus_1 = "Слишком много позиций для спарки с белой маркировкой!"
                        write_to_xlsx("Ошибка", "Выход/", text_warn_rus_1)
                        # raise Warning("too many positions for pairing with white marking!")
                elif type(marking) is str and 'ч' in marking.lower():
                    if not no_more_black_pairing:
                        time_spend_black_pairing += time_position
                        if black_pairing_komax == 0:
                            text_warn_rus_1 = "Нет комаксов с возможностью спарки и чёрной маркировкой!"
                            write_to_xlsx("Ошибка", "Выход/", text_warn_rus_1)
                            raise Warning("No komaxes with black marking and pairing ability")
                        df.iloc[row, cols - 1] = black_pairing_komax
                    else:
                        text_warn_rus_1 = "Слишком много позиций для спарки с чёрной маркировкой!"
                        write_to_xlsx("Ошибка", "Выход/", text_warn_rus_1)
                        # raise Warning("too many positions for pairing with black marking!")
                elif marking is None:
                    # count whether more white or black paired komaxes
                    if black_pairing_komax_more:
                        if not no_more_black_pairing and black_pairing_komax != 0:
                            time_spend_black_pairing += time_position
                            df.iloc[row, cols - 1] = black_pairing_komax
                        elif not no_more_white_pairing and white_pairing_komax != 0:
                            time_spend_white_pairing += time_position
                            df.iloc[row, cols - 1] = white_pairing_komax
                        else:
                            text_warn_rus_1 = "Слишком много позиций для спарки без маркировки!"
                            text_warn_rus_2 = "Невозможно их распределить по komax"
                            write_to_xlsx("Ошибка", "Выход/", text_warn_rus_1 + text_warn_rus_2)
                            # raise Warning("too many positions for pairing with no marking!")
                    else:
                        if not no_more_white_pairing and white_pairing_komax != 0:
                            time_spend_white_pairing += time_position
                            df.iloc[row, cols - 1] = white_pairing_komax
                        elif not no_more_black_pairing and black_pairing_komax != 0:
                            time_spend_black_pairing += time_position
                            df.iloc[row, cols - 1] = black_pairing_komax

                        else:
                            text_warn_rus_1 = "Слишком много позиций для спарки без маркировки!"
                            text_warn_rus_2 = "Невозможно их распределить по komax"
                            write_to_xlsx("Ошибка", "Выход/", text_warn_rus_1 + text_warn_rus_2)
                            # raise Warning("too many positions for pairing with no marking!")

                last_row = row == rows - 1
                if time_spend_black_pairing > worker_time or last_row:
                    if black_pairing_komax == 0:
                        text_warn_rus_1 = "Нет komax с чёрной маркировкой и возможностью спарки!"
                        write_to_xlsx("Ошибка", "Выход/", text_warn_rus_1)
                        raise Warning("No komaxes with black marking and pairing ability at all!")
                    alloc[black_pairing_komax][0] += time_spend_black_pairing
                    if not last_row:
                        for key, item in komaxes.items():
                            komax_work = komaxes[key][0] == 1
                            komax_black = komaxes[key][1] == 2
                            komax_pair = komaxes[key][2] == 1
                            current_komax = key == black_pairing_komax
                            less_worker_time = alloc[key][0] < worker_time
                            if komax_work and komax_black and komax_pair and not current_komax and less_worker_time:
                                black_pairing_komax = key
                                time_spend_black_pairing = 0
                                break
                            else:
                                no_more_black_pairing = True

                if time_spend_white_pairing > worker_time or last_row:
                    if white_pairing_komax == 0:
                        text_warn_rus_1 = "Нет комаксов с возможностью спаривания и белой маркировкой!"
                        write_to_xlsx("Ошибка", "Выход/", text_warn_rus_1)
                        raise Warning("No komaxes with white marking and pairing ability at all!")
                    alloc[white_pairing_komax][0] += time_spend_white_pairing
                    if not last_row:
                        for key, item in komaxes.items():
                            komax_work = komaxes[key][0] == 1
                            komax_white = komaxes[key][1] == 1
                            komax_pair = komaxes[key][2] == 1
                            current_komax = key == white_pairing_komax
                            less_worker_time = alloc[key][0] < worker_time
                            if komax_work and komax_white and komax_pair and not current_komax and less_worker_time:
                                white_pairing_komax = key
                                time_spend_black_pairing = 0
                                break
                            else:
                                no_more_white_pairing = True

    # count time for non-paired positions

    time_spend_black = 0
    time_spend_white = 0

    no_more_black = False
    no_more_white = False

    for row in range(1, rows):
        value = df.iloc[row, length2]
        if value is None:
            harness = df.ix[row, harness_number_col]

            quantity_harness = 1
            try:
                quantity_harness = quantity[harness]
            except KeyError:
                text_warn_rus_1 = "Проверь номера жгутов в файле кол-ва жгутов."
                text_warn_rus_2 = "Не найден жгут номер {}".format(harness)
                write_to_xlsx("Ошибка", "Выход/", text_warn_rus_1 + text_warn_rus_2)
                raise KeyError("Check if harness number is correct in \"quantity.xlsx\" file! : {}".format(harness))

            time_position = time_changeover(df, row, column_numbers, time, volume=quantity_harness)

            df.iloc[row, cols - 2] = quantity_harness

            marking = df.iloc[row, mark_col]
            if type(marking) is str and 'б' in marking.lower():
                if not no_more_white:
                    time_spend_white += time_position
                    if white_komax == 0:
                        text_warn_rus_1 = "Нет komax с белой маркировкой!"
                        write_to_xlsx("Ошибка", "Выход/", text_warn_rus_1)
                        raise Warning("No komaxes with white marking")
                    df.iloc[row, cols - 1] = white_komax
                else:
                    text_warn_rus_1 = "Не хватает komax с белой маркировкой"
                    write_to_xlsx("Ошибка", "Выход/", text_warn_rus_1)
                    # raise Warning("too many positions with white marking!")
            elif type(marking) is str and 'ч' in marking.lower():
                if not no_more_black:
                    time_spend_black += time_position
                    if black_komax == 0:
                        text_warn_rus_1 = "Нет komax с чёрной маркировкой!"
                        write_to_xlsx("Ошибка", "Выход/", text_warn_rus_1)
                        raise Warning("No komaxes with black marking")
                    df.iloc[row, cols - 1] = black_komax
                else:
                    text_warn_rus_1 = "Не хватает komax с чёрной маркировкой!"
                    write_to_xlsx("Ошибка", "Выход/", text_warn_rus_1)
                    # raise Warning("too many positions with black marking!")
            elif marking is None:
                if black_komax_more:
                    if not no_more_black and black_komax != 0:
                        time_spend_black += time_position
                        df.iloc[row, cols - 1] = black_komax
                    elif not no_more_white and white_komax != 0:
                        time_spend_white += time_position
                        df.iloc[row, cols - 1] = white_komax
                    else:
                        text_warn_rus_1 = "Не хватает komax для не маркированных позиций"
                        write_to_xlsx("Ошибка", "Выход/", text_warn_rus_1)
                        # raise Warning("too many positions with no marking!")
                else:
                    if not no_more_white and white_komax != 0:
                        time_spend_white += time_position
                        df.iloc[row, cols - 1] = white_komax
                    elif not no_more_black and black_komax != 0:
                        time_spend_black += time_position
                        df.iloc[row, cols - 1] = black_komax
                    else:
                        text_warn_rus_1 = "Не хватает komax для не маркированных позиций"
                        write_to_xlsx("Ошибка", "Выход/", text_warn_rus_1)
                        # raise Warning("too many positions with no marking!")

            last_row = row == rows - 1
            if time_spend_black > worker_time or last_row:
                if black_komax == 0:
                    text_warn_rus_1 = "Нет komax с чёрной маркировкой вообще!"
                    write_to_xlsx("Ошибка", "Выход/", text_warn_rus_1)
                    raise Warning("No komaxes with black marking at all!")
                alloc[black_komax][0] += time_spend_black
                if not last_row:
                    black_komax_copy = black_komax
                    # find some free komax without pairing
                    for key, item in komaxes.items():
                        komax_work = komaxes[key][0] == 1
                        komax_black = komaxes[key][1] == 2
                        komax_pair = komaxes[key][2] == 1
                        current_komax = key == black_komax
                        less_worker_time = alloc[key][0] < worker_time
                        if komax_work and komax_black and not komax_pair and not current_komax and less_worker_time:
                            black_komax = key
                            time_spend_black = 0
                            break
                    # if not found, so find some pairing komax that is not fully loaded
                    if black_komax == black_komax_copy:
                        for key, item in komaxes.items():
                            komax_work = komaxes[key][0] == 1
                            komax_black = komaxes[key][1] == 2
                            komax_pair = komaxes[key][2] == 1
                            less_worker_time = komaxes[key][0] < worker_time
                            current_key = key == black_komax
                            if komax_work and komax_black and komax_pair and not current_key and less_worker_time:
                                black_komax = key
                                time_spend_black = 0
                                break
                        if black_komax == black_komax_copy:
                            no_more_black = True

            if time_spend_white > worker_time or last_row:
                if white_komax == 0:
                    text_warn_rus_1 = "Нет komax с белой маркировкой"
                    write_to_xlsx("Ошибка", "Выход/", text_warn_rus_1)
                    raise Warning("No komaxes with white marking at all")
                alloc[white_komax][0] += time_spend_white
                if not last_row:
                    white_komax_copy = white_komax
                    # find some free komax without pairing
                    for key, item in komaxes.items():
                        komax_work = komaxes[key][0] == 1
                        komax_black = komaxes[key][1] == 2
                        komax_pair = komaxes[key][2] == 1
                        current_komax = key == white_komax
                        less_worker_time = alloc[key][0] < worker_time
                        if komax_work and not komax_black and not komax_pair and not current_komax and less_worker_time:
                            white_komax = key
                            time_spend_white = 0
                            break
                    # if not found, so find some pairing komax that is not fully loaded
                    if white_komax == white_komax_copy:
                        for key, item in komaxes.items():
                            komax_work = komaxes[key][0] == 1
                            komax_black = komaxes[key][1] == 2
                            komax_pair = komaxes[key][2] == 1
                            less_worker_time = komaxes[key][0] < worker_time
                            current_key = key == white_komax
                            if komax_work and not komax_black and komax_pair and not current_key and less_worker_time:
                                white_komax = key
                                time_spend_white = 0
                                break
                        if white_komax == white_komax_copy:
                            no_more_white = True
        else:
            pass

    return alloc

