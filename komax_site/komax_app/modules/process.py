import pandas as pd
import random

class ProcessDataframe:
    chart = None
    chart_copy = None
    new_chart = None


    __cols_name = {
        "wire_terminal_1": "wire_terminal_2",
        "wire_seal_1": "wire_seal_2",
        "wire_cut_length_1": "wire_cut_length_2",
        "aplicator_1": "aplicator_2",
        "armirovka_1": "armirovka_2",
        "tube_len_1": "tube_len_2",
    }

    def __init__(self, dataframe):
        self.chart = dataframe
        self.chart_copy = dataframe
        self.new_chart = pd.DataFrame()

    def __swap_sides(self, rows, cols=None, copy=False):
        if cols is None:
            cols = self.__cols_name
        for row in rows:
            for key, item in cols.items():

                if copy:
                    self.chart_copy.loc[row, [key, item]] = self.chart_copy.loc[row, [item, key]].values
                else:
                    self.chart.loc[row, [key, item]] = self.chart.loc[row, [item, key]].values

    def delete_word_contain(self, *args):
        columns = list(self.chart)
        for idx, row in self.chart.iterrows():
            for arg in args:
                for column in columns:
                    value = self.chart.loc[idx, column]
                    type_cell = type(value)
                    if type_cell is str and type(arg) is str:
                        if str(arg) in value or arg in value:
                            self.chart.loc[idx, column] = ''
                    elif (type_cell is int or float) and (type(arg) is int or float) and value == arg:
                        self.chart.loc[idx, column] = 0

    def __swap_cols(self, col1, col2):
        filtered = []
        second_filtered = []
        rows, cols = self.chart.shape
        rows_to_swap = []

        """
        h3 = -1
        if pairing:
            try:
                h3 = get_index(df, "Наконечник 3")[0]
            except:
                h3 = -1
        """

        for index, row in self.chart.iterrows():
            """
            if pairing and h3 != -1:
                if df.iloc[row, h3] is not None:
                    filtered.append(df.iloc[row, col1])
            """
            if self.chart.loc[index, col1] not in filtered:
                main_word = self.chart.loc[index, col1]
                if not empty(main_word) and main_word not in second_filtered:
                    filtered.append(main_word)
                    for idx, row_content in self.chart.iterrows():
                        left_word = self.chart.loc[idx, col1]
                        right_word = self.chart.loc[idx, col2]

                        if right_word == main_word and right_word != left_word and left_word not in filtered and \
                                idx not in rows_to_swap:
                            if not empty(left_word) and left_word not in second_filtered:
                                print(idx, left_word)
                                second_filtered.append(left_word)
                            rows_to_swap.append(idx)
                        elif left_word in filtered and index not in rows_to_swap:
                            if not empty(right_word) and right_word not in second_filtered:
                                second_filtered.append(right_word)
                elif not empty(main_word) and main_word in second_filtered and index not in rows_to_swap:
                    right_word = self.chart.loc[index, col2]
                    if right_word not in second_filtered:
                        rows_to_swap.append(index)
            else:
                right_word = self.chart.loc[index, col2]
                if not empty(right_word) and right_word not in second_filtered:
                    second_filtered.append(right_word)

        self.__swap_sides(rows_to_swap)

        """
        rows_to_swap_second = []
        for index, row in self.chart.iterrows():
            main_word = self.chart.loc[index, col1]
            ax_word = self.chart.loc[index, col2]
            if main_word in second_filtered and ax_word not in second_filtered and index not in rows_to_swap:
                rows_to_swap_second.append(index)

        self.__swap_sides(rows_to_swap_second)"""

    def __swap_cols_gaps(self, col1, col2):
        rows_to_swap = []
        rows = self.chart.shape[0]

        main_value = None
        for idx, row in self.chart.iterrows():
            if idx != rows - 1:
                curr_sec_value = self.chart.loc[idx, col2]
                curr_first_value = self.chart.loc[idx, col1]
                next_first_value = self.chart.loc[idx + 1, col1]

                if next_first_value == '' or next_first_value == ' ' or next_first_value is None:
                    if main_value is None:
                        main_value = curr_first_value
                elif curr_first_value != '' and curr_first_value != ' ' and curr_first_value is not None:
                    main_value = None

                if main_value is not None:
                    if curr_sec_value == main_value:
                        rows_to_swap.append(idx)

        self.__swap_sides(rows_to_swap)

    def __swap_rows(self, row1, row2):
        b, c = self.chart.iloc[row1].copy(), self.chart.iloc[row2].copy()
        self.chart.iloc[row1], self.chart.iloc[row2] = c, b

    def __divide_in_groups(self):
        self.chart['groups'] = ''

        for index, row in self.chart.iterrows():
            self.chart.loc[index, 'groups'] = str(group_by(self.chart.loc[index, 'wire_square']))

    def __correct_marking(self):
        MARKING_COL = 'marking'

        for index, row in self.chart.iterrows():
            mark = self.chart.loc[index, MARKING_COL]

            if mark.lower() == 'чёрный' or mark.lower() == 'черный':
                self.chart.loc[index, MARKING_COL] = 'чёрный'

    def __fulfill_terminals(self):
        MARKING_COL = 'marking'
        list_1 = []
        list_2 = []
        first = {}
        second = {}

        for idx, row in self.chart.iterrows():
            value_1 = self.chart.loc[idx, 'wire_terminal_1']
            group = self.chart.loc[idx, 'groups']
            value_2 = self.chart.loc[idx, 'wire_terminal_2']
            marking = self.chart.loc[idx, MARKING_COL]

            if empty(value_1):
                for idx_local, row_local in self.chart.iterrows():
                    same_group = group == self.chart.loc[idx_local, 'groups']
                    diff_indexes = idx_local != idx
                    same_value = self.chart.loc[idx_local, 'wire_terminal_2'] == value_2
                    value_tmp = self.chart.loc[idx_local, 'wire_terminal_1']
                    same_mark = marking.lower() == self.chart.loc[idx_local, MARKING_COL].lower()

                    if diff_indexes and same_value and same_group and not empty(value_tmp) and same_mark:
                        list_1.append(idx)
                        first[idx] = value_tmp
                        # self.chart.loc[idx, 'wire_terminal_1'] = value_tmp
                        break

            if empty(value_2):
                for idx_local, row_local in self.chart.iterrows():
                    same_group = group == self.chart.loc[idx_local, 'groups']
                    diff_indexes = idx_local != idx
                    same_value = value_1 == self.chart.loc[idx_local, 'wire_terminal_1']
                    value_tmp = self.chart.loc[idx_local, 'wire_terminal_2']
                    same_mark = marking.lower() == self.chart.loc[idx_local, MARKING_COL].lower()
                    if diff_indexes and same_value and same_group and not empty(value_tmp) and same_mark:
                        list_2.append(idx)
                        second[idx] = value_tmp
                        # self.chart.loc[idx, 'wire_terminal_2'] = value_tmp
                        break

        for index, row in self.chart.iterrows():
            if index in first:
                self.chart.loc[index, 'wire_terminal_1'] = first[index]
            if index in second:
                self.chart.loc[index, 'wire_terminal_2'] = second[index]

        return (list_1, list_2)

    def __swap_cols_after(self, col1, col2):
        rows_to_swap = []

        for index, row in self.chart.iterrows():
            ax_value = self.chart.loc[index, col2]
            if ax_value is None or ax_value == '' or ax_value == ' ':
                main_value = self.chart.loc[index, col1]
                for idx, row in self.chart.iterrows():
                    if idx > index:
                        ax_value_tmp = self.chart.loc[idx, col2]
                        if ax_value_tmp == main_value:
                            rows_to_swap.append(index)

        self.__swap_sides(rows_to_swap)

    def __reset_index(self):
        self.chart.index = pd.Index(range(self.chart.shape[0]))

    def sort(self, method='simple', first_sort=False, test=False):
        self.delete_word_contain('*')

        self.__correct_marking()
        self.chart.sort_values(
            by=['marking'],
            ascending=True,
            inplace=True
        )
        self.__reset_index()

        if test:
            self.chart.to_excel('test0.xlsx')

        self.__swap_cols('wire_terminal_1', 'wire_terminal_2')

        self.__reset_index()

        self.__divide_in_groups()
        pairing_required = str(int('wire_terminal_3' in self.chart.columns))

        if test:
            self.chart.to_excel('test.xlsx')

        idxs_1, idxs_2 = self.__fulfill_terminals()
        self.chart.to_excel('test1.xlsx')
        if first_sort:
            self.chart.sort_values(
                by=['marking', 'groups', 'wire_terminal_1', 'wire_terminal_2', 'wire_square', 'wire_color'],
                ascending=True,
                inplace=True
            )
        else:
            self.chart.sort_values(
                by=['marking', 'groups', 'wire_terminal_2', 'wire_terminal_1', 'wire_square', 'wire_color'],
                ascending=True,
                inplace=True
            )

        if test:
            self.chart.to_excel('test2.xlsx')

        for idx in idxs_1:
            self.chart.loc[idx, 'wire_terminal_1'] = ''
        for idx in idxs_2:
            self.chart.loc[idx, 'wire_terminal_2'] = ''

        self.__reset_index()

        if method == 'double':
            # self.__swap_cols_after('wire_terminal_1', 'wire_terminal_2')

            idxs_1, idxs_2 = self.__fulfill_terminals()

            if first_sort:
                self.chart.sort_values(
                    by=['marking', 'groups', 'wire_terminal_1', 'wire_terminal_2', 'wire_square', 'wire_color'],
                    ascending=True,
                    inplace=True
                )
            else:
                self.chart.sort_values(
                    by=['marking', 'groups', 'wire_terminal_2', 'wire_terminal_1', 'wire_square', 'wire_color'],
                    ascending=True,
                    inplace=True
                )



            self.__reset_index()

            self.chart.to_excel('test.xlsx')
            for idx in idxs_1:
                self.chart.loc[idx, 'wire_terminal_1'] = ''
            for idx in idxs_2:
                self.chart.loc[idx, 'wire_terminal_2'] = ''

            # self.__swap_cols_gaps('wire_terminal_2', 'wire_terminal_1')

        self.chart.drop(
            columns=['groups'],
            inplace=True
        )

        self.__reset_index()

    def __time_changeover(self, idx, time, volume=1, last_first=None, last_second=None, pairing=False, full=False,
                          last_index=None, swapped=False):
        square_change, color_change, conn1_change, conn2_change = False, False, False, False
        armirovka1_change, armirovka2_change = False, False
        time_position = 0

        if full:
            return time['learn'] * 3 + time['aplicator'] * 2 + time['direction'] + time['contact'] * 2 + time['wire'] +\
                   time['compact'] + time['pack'] + time['ticket'] + time['task'] + time['cut'] * volume

        if not pairing:
            if last_index is not None and swapped:
                self.__swap_sides([idx], copy=True)

            cols = list(self.chart)
            for col in cols:
                value = self.chart.loc[idx, col]
                if idx > 0:
                    if last_index is None:
                        back_value = self.chart.loc[idx - 1, col]
                    else:
                        back_value = self.new_chart.loc[last_index, col]

                    if value != back_value:
                        if col == 'wire_color':
                            color_change = True
                        elif col == 'wire_square':
                            square_change = True
                        elif col == 'wire_terminal_1':
                            if value is not None and value != '' and value != ' ':
                                if back_value is None or back_value == '' or back_value == ' ':
                                    if last_first is not None and last_first == value:
                                        conn1_change = False
                                    else:
                                        conn1_change = True
                                else:
                                    conn1_change = True
                            else:
                                conn1_change = False
                        elif col == 'wire_terminal_2':
                            if value is not None and value != '' and value != ' ':
                                if back_value is None or back_value == '' or back_value == ' ':
                                    if last_second is not None and last_second == value:
                                        conn2_change = False
                                    else:
                                        conn2_change = True
                                else:
                                    conn2_change = True
                            else:
                                conn2_change = False
                        elif col == 'wire_seal_1':
                            if value is not None and value != '' and value != ' ':
                                if back_value is None or back_value == '' or back_value == ' ':
                                    if conn1_change:
                                        armirovka1_change = True
                                    else:
                                        armirovka1_change = False
                                else:
                                    armirovka1_change = True
                            else:
                                armirovka1_change = False
                        elif col == 'wire_seal_2' and value is not None and value != '':
                            if value is not None and value != '' and value != ' ':
                                if back_value is None or back_value == '' or back_value == ' ':
                                    if conn2_change:
                                        armirovka2_change = True
                                    else:
                                        armirovka2_change = False
                                else:
                                    armirovka2_change = True
                            else:
                                armirovka2_change = False
                else:
                    color_change, square_change, conn1_change, conn2_change = True, True, True, True
                    armirovka2_change, armirovka1_change = True, True

            if last_index is not None and swapped:
                self.__swap_sides([idx], copy=True)

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

            if square_change:
                time_position += time['compact']

            if armirovka1_change:
                time_position += time['compact']
            if armirovka2_change:
                time_position += time['compact']


            time_position += (time['pack'] + time['ticket'] + time['task'])

            time_position += volume * time['cut']
        else:
            time_position = time['aplicator']

        return time_position

    def smart_sort(self, time, amount):
        HARNESS_NUMBER_COL = "harness"
        base_rows = self.chart_copy.shape[0]
        sum_time = 0
        min_time = 0

        self.new_chart['Amount'] = 0

        for base_row in range(base_rows):
            main_row = self.new_chart.shape[0] - 1

            if base_row == 0:
                idx = random.randint(0, base_rows - 1)
                self.new_chart = self.new_chart.append(self.chart_copy.loc[idx, :])
                self.new_chart.index = pd.Index(range(self.new_chart.shape[0]))
                volume = amount[self.chart_copy.loc[idx, HARNESS_NUMBER_COL]]
                self.new_chart.loc[base_row, 'Amount'] = volume
                self.chart_copy.drop(index=idx, inplace=True)
                continue

            if base_row != main_row and main_row >= 0:
                min_time = 10000
                min_index = 0
                to_swap = False
                for index, row in self.chart_copy.iterrows():
                    volume = amount[self.chart_copy.loc[index, HARNESS_NUMBER_COL]]
                    time1 = self.__time_changeover(index, time, volume=volume, last_index=main_row)
                    time2 = self.__time_changeover(index, time, volume=volume, last_index=main_row, swapped=True)



                    if time1 > time2:
                        if min_time > time2:
                            min_time = time2
                            min_index = index
                            to_swap = True
                    else:
                        if min_time > time1:
                            min_time = time1
                            to_swap = False
                            min_index = index

                if to_swap:
                    self.__swap_sides([min_index], copy=True)

                self.new_chart = self.new_chart.append(self.chart_copy.loc[min_index, :])
                self.new_chart.index = pd.Index(range(self.new_chart.shape[0]))
                volume = amount[self.chart_copy.loc[min_index, HARNESS_NUMBER_COL]]
                self.new_chart.loc[base_row, 'Amount'] = volume
                self.chart_copy.drop(index=min_index, inplace=True)

            sum_time += min_time

        return sum_time

    #TODO : big time needed, incorrect algo, too many changeovers
    def task_allocate(self, komaxes, quantity, time, hours):

        """
        required quicksort with params: pairing-marking-square-terminal-terminal

        :param komaxes: {komax_number : komax_status(0, 1), komax_marking(1 - w, 2 - b), komax_pairing (0, 1)
        :param quantity: {harness_number : amount}
        :param time: {ops name : time(sec)}
        :param hours: hours
        :return: {komax_number : loaded_time(sec)}
        """

        HARNESS_NUMBER_COL = "harness"
        KOMAX_COL = 'komax'
        MARKING_COL = "marking"
        HOURS_TO_SEC = 3600

        self.chart[KOMAX_COL] = ''

        alloc = {i : 0 for i in range(1, len(komaxes) + 1)}

        curr_marking = 0
        curr_pairing = 0
        curr_group_terminal = ''
        idx_start = 0
        time_changeover = 0

        first_sort = self.chart.nunique()["wire_terminal_1"] >= self.chart.nunique()["wire_terminal_2"]

        list_groups = {}

        for idx, row in self.chart.iterrows():
            charachteristic_value = row['col_for_sort'].split(' ')

            new_marking = charachteristic_value[1] != curr_marking
            new_pairing = charachteristic_value[0] != curr_pairing
            new_group_terminal = charachteristic_value[3] != curr_group_terminal
            last_idx = idx == len(self.chart)

            curr_marking = 1 if 'белый' in charachteristic_value[1].lower() else 2
            curr_pairing = int(charachteristic_value[0])
            curr_group_terminal = charachteristic_value[3]

            volume = quantity[self.chart.loc[idx, HARNESS_NUMBER_COL]]

            if new_marking or new_pairing or new_group_terminal:
                if not last_idx:
                    list_groups[idx_start] = [curr_pairing, curr_marking, time_changeover, idx]
                else:
                    time_changeover += self.__time_changeover(idx, time, volume, curr_pairing)
                    list_groups[idx_start] = [curr_pairing, curr_marking, time_changeover, idx + 1]

                time_changeover = 0

                idx_start = idx
                time_changeover += self.__time_changeover(idx, time, volume, curr_pairing, full=True)
            else:
                time_changeover += self.__time_changeover(idx, time, volume, curr_pairing)

        for key, item in list_groups.items():
            for komax_num, komax_set in komaxes.items():
                has_free_time = hours * HOURS_TO_SEC - alloc[komax_num] > item[2]
                pairing = komax_set[2] == item[0]
                marking = komax_set[1] == item[1]
                working = komax_set[0] != 0

                if has_free_time and pairing and marking and working:
                    idx_start = key
                    idx_end = item[3]
                    for idx in range(idx_start, idx_end):
                        self.chart.loc[idx, KOMAX_COL] = komax_num
                    alloc[komax_num] += float(item[2])
                elif not has_free_time and pairing and marking and working:
                    free_time_all = 0
                    komax_set = {}
                    for komax_num_local, komax_set_local in komaxes.items():
                        has_free_time = hours * HOURS_TO_SEC - alloc[komax_num_local] > item[2]
                        pairing = komax_set_local[2] == item[0]
                        marking = komax_set_local[1] == item[1]
                        working = komax_set_local[0] != 0
                        if has_free_time and pairing and marking and working:
                            free_time_local = hours * HOURS_TO_SEC - alloc[komax_num_local]
                            if komax_num_local in komax_set.keys():
                                komax_set[komax_num_local] += free_time_local
                            else:
                                komax_set[komax_num_local] = free_time_local
                            free_time_all += hours * HOURS_TO_SEC - alloc[komax_num_local]

                    if free_time_all < item[2]:
                        # means that for this group free time of all komaxes less than required to cut this group
                        return -1
                    else:
                        idx_start_local = key
                        idx_end_local = item[3]
                        for komax_num_local, komax_free_time in komax_set.items():
                            # better get last row and count time of changeover better, but
                            # will count as full

                            for idx_local in range(idx_start_local, idx_end_local):
                                volume = quantity[self.chart.loc[idx_local, HARNESS_NUMBER_COL]]
                                time_changeover_local = 0
                                if idx_local == idx_start_local:
                                    time_changeover_local = self.__time_changeover(idx_local, time, volume, pairing, True)
                                else:
                                    time_changeover_local = self.__time_changeover(idx_local, time, volume, pairing)

                                komax_free_time -= time_changeover_local
                                if komax_free_time > 0:
                                    self.chart.loc[idx_local, KOMAX_COL] = komax_num_local
                                else:
                                    komax_free_time += time_changeover_local
                                    idx_start_local = idx_local
                                    break

                        if self.chart.loc[idx_end_local - 1] == '':
                            # means that end of komaxes
                            return -2

        return alloc

    #TODO : incorrect changeover counting
    def task_allocation(self, komaxes, quantity, time, hours):
        HARNESS_NUMBER_COL = "harness"
        AMOUNT_COL = "Amount"
        KOMAX_COL = 'komax'
        MARKING_COL = "marking"
        TERMINAL_1_COL = 'wire_terminal_1'
        TERMINAL_2_COL = 'wire_terminal_2'


        """
        try:
            length2 = get_index(df, "Длина, мм (± 3мм) 2")[0]
        except TypeError:
            length2 = -1
        """

        # create dict of allocation
        alloc = {i: [0] for i in komaxes}
        worker_time = hours*60*60       # in seconds

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

        # adding columns with harnesses amount and komax number alloc

        self.chart[AMOUNT_COL] = ''
        self.chart[KOMAX_COL] = ''

        #count time for paired positions
        """
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
        """

        # count time for non-paired positions

        time_spend_black = 0
        time_spend_white = 0

        no_more_black = False
        no_more_white = False

        first_black = False
        first_white = False

        print(self.chart[:5])
        print(MARKING_COL, first_black, first_white)
        print(self.chart.loc[:2, MARKING_COL])
        for idx, row in self.chart.iterrows():

            # value = df.iloc[row, length2]
            value = None
            if value is None:
                harness = self.chart.loc[idx, HARNESS_NUMBER_COL]

                quantity_harness = 1
                quantity_harness = quantity[harness]
                """
                try:
                    quantity_harness = quantity[harness]
                except KeyError:
                    raise KeyError("Check if harness number is correct in \"quantity.xlsx\" file! : {}".format(harness))
                """

                if ('черный' or 'чёрный') in self.chart.loc[idx, MARKING_COL].lower() and not first_black:
                    first_black = True
                    time_position = self.__time_changeover(idx, time, volume=quantity_harness, full=True)
                elif 'белый' in self.chart.loc[idx, MARKING_COL].lower() and not first_white:
                    first_white = True
                    time_position = self.__time_changeover(idx, time, volume=quantity_harness, full=True)
                else:
                    #TODO: Try to make func for this part
                    print(idx, self.chart.loc[idx, MARKING_COL].lower(), first_black, first_white)
                    back_first_col_value = self.chart.loc[idx - 1, TERMINAL_1_COL]
                    first_col_value = self.chart.loc[idx, TERMINAL_1_COL]

                    back_second_col_value = self.chart.loc[idx - 1, TERMINAL_2_COL]
                    second_col_value = self.chart.loc[idx, TERMINAL_2_COL]

                    last_second, last_first = None, None

                    if back_first_col_value is None or back_first_col_value == ' ' or back_first_col_value == '':
                        if first_col_value is not None and first_col_value != ' ' and first_col_value != '':
                            index = idx - 1
                            while index > 0:
                                if back_first_col_value is not None and back_first_col_value != ' ' and back_first_col_value != '':
                                    break
                                else:
                                    index -= 1
                                back_first_col_value = self.chart.loc[index, TERMINAL_1_COL]
                            last_first = self.chart.loc[index, TERMINAL_1_COL]
                    if back_second_col_value is None or back_second_col_value == ' ' or back_second_col_value == '':
                        if second_col_value is not None and second_col_value != ' ' and second_col_value != '':
                            index = idx - 1
                            while index > 0:
                                if back_second_col_value is not None and back_second_col_value != ' ' and back_second_col_value != '':
                                    break
                                else:
                                    index -= 1
                                back_second_col_value = self.chart.loc[index, TERMINAL_2_COL]
                            last_second = self.chart.loc[index, TERMINAL_2_COL]

                    time_position = self.__time_changeover(idx, time, volume=quantity_harness,
                                                           last_first=last_first, last_second=last_second)

                self.chart.loc[idx, AMOUNT_COL] = quantity_harness
                marking = self.chart.loc[idx, MARKING_COL]

                if type(marking) is str and 'б' in marking.lower():
                    if not no_more_white:
                        time_spend_white += time_position
                        if white_komax == 0:
                            pass
                            # raise Warning("No komaxes with white marking")
                        self.chart.loc[idx, KOMAX_COL] = white_komax
                    else:
                        # raise Warning("too many positions with white marking!")
                        return -1
                elif type(marking) is str and 'ч' in marking.lower():
                    if not no_more_black:
                        time_spend_black += time_position
                        if black_komax == 0:
                            # raise Warning("No komaxes with black marking")
                            pass
                        self.chart.loc[idx, KOMAX_COL] = black_komax
                    else:
                        # raise Warning("too many positions with black marking!")
                        return -1
                elif marking is None:
                    if black_komax_more:
                        if not no_more_black and black_komax != 0:
                            time_spend_black += time_position
                            self.chart.loc[idx, KOMAX_COL] = black_komax
                        elif not no_more_white and white_komax != 0:
                            time_spend_white += time_position
                            self.chart.loc[idx, KOMAX_COL] = white_komax
                        else:
                            # raise Warning("too many positions with no marking!")
                            return -1
                    else:
                        if not no_more_white and white_komax != 0:
                            time_spend_white += time_position
                            self.chart.loc[idx, KOMAX_COL] = white_komax
                        elif not no_more_black and black_komax != 0:
                            time_spend_black += time_position
                            self.chart.loc[idx, KOMAX_COL] = black_komax
                        else:
                            # raise Warning("too many positions with no marking!")
                            return -1

                last_row = idx == len(self.chart) - 1
                if time_spend_black > worker_time or last_row:
                    if black_komax == 0:
                        # raise Warning("No komaxes with black marking at all!")
                        return -1
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
                        # raise Warning("No komaxes with white marking at all")
                        return -1
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

    def task_allocation_base(self, komaxes, quantity, time, hours):

        HARNESS_NUMBER_COL = "harness"
        AMOUNT_COL = "Amount"
        KOMAX_COL = 'komax'
        MARKING_COL = "marking"
        TERMINAL_1_COL = 'wire_terminal_1'
        TERMINAL_2_COL = 'wire_terminal_2'


        """
        try:
            length2 = get_index(df, "Длина, мм (± 3мм) 2")[0]
        except TypeError:
            length2 = -1
        """

        # create dict of allocation
        alloc = {i: [0] for i in komaxes}
        worker_time = hours*60*60       # in seconds

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

        # adding columns with harnesses amount and komax number alloc

        self.chart[AMOUNT_COL] = ''
        self.chart[KOMAX_COL] = ''

        #count time for paired positions
        """
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
        """

        # count time for non-paired positions

        time_spend_black = 0
        time_spend_white = 0

        no_more_black = False
        no_more_white = False

        first_black = False
        first_white = False

        for idx, row in self.chart.iterrows():
            # value = df.iloc[row, length2]
            value = None
            if value is None:
                harness = self.chart.loc[idx, HARNESS_NUMBER_COL]

                quantity_harness = quantity[harness]
                """
                try:
                    quantity_harness = quantity[harness]
                except KeyError:
                    raise KeyError("Check if harness number is correct in \"quantity.xlsx\" file! : {}".format(harness))
                """

                if ('черный' or 'чёрный') in self.chart.loc[idx, MARKING_COL].lower() and not first_black:
                    first_black = True
                    time_position = self.__time_changeover(idx, time, volume=quantity_harness, full=True)
                elif 'белый' in self.chart.loc[idx, MARKING_COL].lower() and not first_white:
                    first_white = True
                    time_position = self.__time_changeover(idx, time, volume=quantity_harness, full=True)
                else:
                    #TODO: Try to make func for this part
                    back_first_col_value = self.chart.loc[idx - 1, TERMINAL_1_COL]
                    first_col_value = self.chart.loc[idx, TERMINAL_1_COL]

                    back_second_col_value = self.chart.loc[idx - 1, TERMINAL_2_COL]
                    second_col_value = self.chart.loc[idx, TERMINAL_2_COL]

                    last_second, last_first = None, None

                    if back_first_col_value is None or back_first_col_value == ' ' or back_first_col_value == '':
                        if first_col_value is not None and first_col_value != ' ' and first_col_value != '':
                            index = idx - 1
                            while index > 0:
                                if back_first_col_value is not None and back_first_col_value != ' ' and back_first_col_value != '':
                                    break
                                else:
                                    index -= 1
                                back_first_col_value = self.chart.loc[index, TERMINAL_1_COL]
                            last_first = self.chart.loc[index, TERMINAL_1_COL]
                    if back_second_col_value is None or back_second_col_value == ' ' or back_second_col_value == '':
                        if second_col_value is not None and second_col_value != ' ' and second_col_value != '':
                            index = idx - 1
                            while index > 0:
                                if back_second_col_value is not None and back_second_col_value != ' ' and back_second_col_value != '':
                                    break
                                else:
                                    index -= 1
                                back_second_col_value = self.chart.loc[index, TERMINAL_2_COL]
                            last_second = self.chart.loc[index, TERMINAL_2_COL]

                    time_position = self.__time_changeover(idx, time, volume=quantity_harness,
                                                           last_first=last_first, last_second=last_second)

                self.chart.loc[idx, AMOUNT_COL] = quantity_harness
                marking = self.chart.loc[idx, MARKING_COL]

                if type(marking) is str and 'б' in marking.lower():
                    if not no_more_white:
                        time_spend_white += time_position
                        if white_komax == 0:
                            pass
                            # raise Warning("No komaxes with white marking")
                        else:
                            self.chart.loc[idx, KOMAX_COL] = white_komax
                    else:
                        # raise Warning("too many positions with white marking!")
                        pass
                elif type(marking) is str and 'ч' in marking.lower():
                    if not no_more_black:
                        time_spend_black += time_position
                        if black_komax == 0:
                            # raise Warning("No komaxes with black marking")
                            pass
                        else:
                            self.chart.loc[idx, KOMAX_COL] = black_komax
                    else:
                        # raise Warning("too many positions with black marking!")
                        pass
                elif marking is None:
                    if black_komax_more:
                        if not no_more_black and black_komax != 0:
                            time_spend_black += time_position
                            self.chart.loc[idx, KOMAX_COL] = black_komax
                        elif not no_more_white and white_komax != 0:
                            time_spend_white += time_position
                            self.chart.loc[idx, KOMAX_COL] = white_komax
                        else:
                            # raise Warning("too many positions with no marking!")
                            pass
                    else:
                        if not no_more_white and white_komax != 0:
                            time_spend_white += time_position
                            self.chart.loc[idx, KOMAX_COL] = white_komax
                        elif not no_more_black and black_komax != 0:
                            time_spend_black += time_position
                            self.chart.loc[idx, KOMAX_COL] = black_komax
                        else:
                            # raise Warning("too many positions with no marking!")
                            pass

                last_row = idx == len(self.chart) - 1
                if time_spend_black > worker_time or last_row:
                    if black_komax == 0:
                        # raise Warning("No komaxes with black marking at all!")
                        pass
                    else:
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
                        # raise Warning("No komaxes with white marking at all")
                        pass
                    else:
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

def group_by(square):
    if square <= 1.0:
        return 1
    elif square > 1.0 and square <= 2.5:
        return 2
    elif square >2.5:
        return 3

def get_time_from(time_df):
    temp_dict = time_df.to_dict()

    output_dict = {}
    for idx, action in temp_dict['action'].items():
        output_dict[action] = temp_dict['time'][idx]

    return output_dict

def get_komaxes_from(komax_df):
    temp_dict = komax_df.to_dict()
    output_dict = {}

    for idx, komax_num in temp_dict['number'].items():
        status = (1 if temp_dict['status'][idx] == 'Work' else 0)
        marking = (1 if temp_dict['marking'][idx] == 'White' else 2)
        pairing = (1 if temp_dict['pairing'][idx] == 'Yes' else 0)


        output_dict[komax_num] = (status, marking, pairing)

    return output_dict

def get_amount_from(amount_df):
    temp_dict = amount_df.to_dict()
    output_dict = {}

    for idx, harness in temp_dict['harness'].items():
        output_dict[harness] = temp_dict['amount'][idx]

    return output_dict

def empty(string):
    return False if string is not None and len(string) > 0 else True

