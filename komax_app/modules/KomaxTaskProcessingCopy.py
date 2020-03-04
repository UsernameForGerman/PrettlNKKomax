class KomaxTaskProcessing():

    def __init__(self):
        return

    def save_obj(self, obj):
        obj.save()

    def get_komax_task(self, task_name):
        return KomaxTask.objects.filter(task_name=task_name)

    def get_harnesses(self, komax_task_obj=None, harness=None):
        if komax_task_obj is None:
            if harness is None:
                return Harness.objects.all()
            else:
                return Harness.objects.filter(harness_number=harness)
        else:
            return komax_task_obj.harnesses.all()

    def get_komaxes(self, komax_task_obj=None, komax=None):
        if komax_task_obj is None:
            if komax is None:
                return Komax.objects.all()
            else:
                return Komax.objects.filter(number=komax)
        else:
            return komax_task_obj.komaxes.all()

    def get_shift(self, komax_task_obj):
        return komax_task_obj.shift

    def get_harness_chart(self, harness_obj=None):
        if harness_obj is not None:
            return HarnessChart.objects.filter(harness=harness_obj)
        else:
            return HarnessChart.objects.all()

    def get_task_personal(self, task_obj=None):
        if task_obj is None:
            return TaskPersonal.objects.all()
        else:
            return TaskPersonal.objects.filter(komax_task=task_obj)

    def get_laboriousness(self):
        return Laboriousness.objects.all()

    def get_kappas(self, kappa_number=1):
        if kappa_number is None:
            return [None, ]
        else:
            return Kappa.objects.filter(number=kappa_number)

    def get_komax_terminls(self):
        return KomaxTerminal.objects.all()

    def load_task_personal(self, komax_task_name):
        komax_task_query = self.get_komax_task(komax_task_name)
        task_personal_loaded_query = TaskPersonal.objects.filter(loaded=True)
        if len(komax_task_query):
            for task_personal in task_personal_loaded_query:
                task_personal.loaded = False
            TaskPersonal.objects.bulk_update(task_personal_loaded_query, ['loaded'])
        if len(komax_task_query):
            komax_task_obj = komax_task_query[0]
            komax_task_obj.loaded = True
            komax_task_obj.save()
        else:
            return

    def create_harness_amount(self, harnesses, amount=-1):
        harness_amount_objs = list()
        for harness in harnesses:
            harness_amount_obj = HarnessAmount(harness=Harness.objects.filter(harness_number=harness)[0], amount=amount)
            harness_amount_objs.append(harness_amount_obj)
            self.save_obj(harness_amount_obj)

        return harness_amount_objs

    def create_komax_time(self, komaxes, time=0):
        komax_time_objs = list()
        for komax in komaxes:
            komax_time_obj = KomaxTime(komax=Komax.objects.filter(number=komax)[0], time=time)
            komax_time_objs.append(komax_time_obj)
            self.save_obj(komax_time_obj)

        return komax_time_objs

    def create_task(self, task_name, harnesses, komaxes, kappas, shift, type_of_allocation):
        harness_amount_objs = self.create_harness_amount(harnesses)
        komax_time_objs = self.create_komax_time(komaxes)
        kappa_obj = None
        if len(kappas):
            kappas_query = self.get_kappas(kappas[0])
            if len(kappas_query):
                kappa_obj = kappas_query[0]
        komax_task_obj = KomaxTask(
            task_name=task_name,
            kappas=kappa_obj,
            shift=shift,
            type_of_allocation=type_of_allocation
        )
        self.save_obj(komax_task_obj)
        komax_task_obj.harnesses.add(*harness_amount_objs)
        komax_task_obj.komaxes.add(*komax_time_objs)
        self.save_obj(komax_task_obj)

        return True

    def update_harness_amount(self, task_name, harness_amount_dict):
        task_query = self.get_komax_task(task_name)
        task = task_query[0]
        harnesses = self.get_harnesses(task)
        for harness in harnesses:
            harness.amount = harness_amount_dict[str(harness)]
            self.save_obj(harness)

        tasks_pers = self.get_task_personal(task)

        for task_pers in tasks_pers:
            task_pers.amount = harness_amount_dict[str(task_pers.harness.harness_number)]
            self.save_obj(task_pers)

    def update_komax_time(self, task_name, komax_time_dict):
        task_query = self.get_komax_task(task_name=task_name)
        task = task_query[0]
        komaxes = self.get_komaxes(komax_task_obj=task)
        for komax in komaxes:
            komax.amount = komax_time_dict[str(komax)]
            self.save_obj(komax)

    def __get_komaxes_from(self, komax_df):
        temp_dict = komax_df.to_dict()
        output_dict = {}
        for idx, komax_num in temp_dict['komax'].items():
            komax = self.get_komaxes(komax=komax_num)[0]
            status = komax.status
            marking = komax.marking
            pairing = komax.pairing
            groups_of_square = tuple(map(int, komax.group_of_square.split()))

            output_dict[int(komax_num)] = (status, marking, pairing, groups_of_square)

        return output_dict

    def sort_komax_task(self, task_name):
        """
        sort komax task
        :param task_name:
        :param type_of_allocation: str, parallel or consistently
        :return:
        """
        task_query = self.get_komax_task(task_name)
        task_obj = task_query[0]
        harnesses_query = self.get_harnesses(komax_task_obj=task_obj)
        komaxes_query = self.get_komaxes(komax_task_obj=task_obj)
        kappas = [task_obj.kappas]

        shift = self.get_shift(task_obj)
        harnesses = harnesses_query

        harness_charts = list()
        for harness in harnesses:
            harness_chart = self.get_harness_chart(harness_obj=harness.harness)
            harness_charts.append(harness_chart)

        df = pd.concat(
            [read_frame(harness_chart) for harness_chart in harness_charts],
            ignore_index=True
        )

        laboriousness = self.get_laboriousness()
        komax_dict = self.__get_komaxes_from(read_frame(komaxes_query))
        time_dict = get_time_from(read_frame(laboriousness))
        type_of_allocation = task_obj.type_of_allocation
        terminals_df = read_frame(self.get_komax_terminls())

        # amount_dict = get_amount_from(read_frame(task_obj.harnesses.all()))

        # print(df, komax_dict, harnesses, time_dict, shift)
        final_data = self.__sort_allocated_task(
            df,
            terminals_df,
            komax_dict,
            kappas,
            harnesses,
            time_dict,
            shift,
            type_of_allocation
        )

        self.sort_alloc_data = final_data

        if final_data['allocation'][0] == -1:
            task_obj.harnesses.all().delete()
            task_obj.komaxes.all().delete()
            task_obj.delete()
            return final_data

        """
        final_data['chart'].drop(
            columns=['tube_len_2', 'tube_len_1', 'armirovka_2', 'armirovka_1', 'id'],
            inplace=True
        )
        """

        for row in final_data['chart'].iterrows():
            row_dict = row[1]
            harness_obj = self.get_harnesses(harness=row_dict['harness'])[0]
            if row_dict['komax'] is None:
                komax_obj = None
            else:
                komax_obj = self.get_komaxes(komax=row_dict['komax'])[0]

            if row_dict['kappa'] is None:
                kappa_obj = None
            else:
                kappa_obj = self.get_kappas(kappa_number=row_dict['kappa'])[0]

            self.save_task_personal(row_dict, task_obj, kappa_obj, harness_obj, komax_obj)

        """
        process = ProcessDataframe(df)
        alloc_base = process.task_allocation_base(komax_dict, amount_dict, time_dict, hours=shift)

        process.delete_word_contain('СВ', 'R')
        first_sort = process.chart.nunique()["wire_terminal_1"] <= process.chart.nunique()["wire_terminal_2"]
        process.sort(method='simple', first_sort=first_sort)
        alloc = process.task_allocation(komax_dict, amount_dict, time_dict, hours=shift)

        first_sort = not first_sort
        new_process = ProcessDataframe(df)
        new_process.sort(method='simple', first_sort=first_sort)
        new_alloc = new_process.task_allocation(komax_dict, amount_dict, time_dict, hours=shift)

        if new_alloc == -1 and alloc == -1:
            task_obj.delete()
            return render(request, 'komax_app/task_status.html')
        elif new_alloc == -1:
            final_alloc = alloc
            final_chart = process.chart
        elif alloc == -1:
            final_alloc = new_alloc
            final_chart = new_process.chart
        else:
            sum_first = sum([i[0] for i in alloc.values()])
            sum_new = sum([i[0] for i in new_alloc.values()])

            if sum_new < sum_first:
                final_chart = new_process.chart
                final_alloc = new_alloc
            else:
                final_chart = process.chart
                final_alloc = alloc

        final_chart.drop(
            columns=['tube_len_2', 'tube_len_1', 'armirovka_2', 'armirovka_1', 'id'],
            inplace=True
        )

        for row in final_chart.iterrows():
            row_dict = row[1]
            task_pers_obj = TaskPersonal(
                task=task_obj,
                harness=get_object_or_404(Harness, harness_number=row_dict['harness']),
                komax=get_object_or_404(Komax, number=row_dict['komax']),
                amount=row_dict["amount"],
                notes=row_dict["notes"],
                marking=row_dict["marking"],
                wire_type=row_dict["wire_type"],
                wire_number=row_dict["wire_number"],
                wire_square=float(row_dict["wire_square"]),
                wire_color=row_dict["wire_color"],
                wire_length=int(row_dict["wire_length"]),
                wire_seal_1=row_dict["wire_seal_1"],
                wire_cut_length_1=float(row_dict["wire_cut_length_1"]),
                wire_terminal_1=row_dict["wire_terminal_1"],
                aplicator_1=row_dict["aplicator_1"],
                wire_seal_2=row_dict["wire_seal_2"],
                wire_cut_length_2=float(row_dict["wire_cut_length_2"]),
                wire_terminal_2=row_dict["wire_terminal_2"],
                aplicator_2=row_dict["aplicator_2"],
            )
            task_pers_obj.save()

        for komax, time in final_alloc.items():
            KomaxTaskAllocation(task=task_obj, komax=get_object_or_404(Komax, number=komax), time=time[0]).save()

        for key, item in final_alloc.items():
            hours = round(final_alloc[key][0] // 3600)
            final_alloc[key] = str(hours) + ':' + str(round((final_alloc[key][0] / 3600 - hours) * 60))

        for key, item in alloc_base.items():
            hours = round(alloc_base[key][0] // 3600)
            alloc_base[key] = str(hours) + ':' + str(round((alloc_base[key][0] / 3600 - hours) * 60))

        for key, item in final_alloc.items():
            final_alloc[key] = [final_alloc[key], alloc_base[key]]
        """
        return final_data

    def save_task_personal(self, row_dict, task_obj, kappa_obj, harness_obj, komax_obj):
        task_pers_obj = TaskPersonal(
            komax_task=task_obj,
            # harness=get_object_or_404(Harness, harness_number=row_dict['harness']),
            # komax=get_object_or_404(Komax, number=row_dict['komax']),
            harness=harness_obj,
            komax=komax_obj,
            kappa=kappa_obj,
            amount=row_dict["amount"],
            notes=row_dict["notes"],
            marking=row_dict["marking"],
            wire_type=row_dict["wire_type"],
            wire_number=row_dict["wire_number"],
            wire_square=float(row_dict["wire_square"]),
            wire_color=row_dict["wire_color"],
            wire_length=int(row_dict["wire_length"]),
            wire_seal_1=row_dict["wire_seal_1"],
            wire_cut_length_1=float(row_dict["wire_cut_length_1"]),
            wire_terminal_1=row_dict["wire_terminal_1"],
            aplicator_1=row_dict["aplicator_1"],
            wire_seal_2=row_dict["wire_seal_2"],
            wire_cut_length_2=float(row_dict["wire_cut_length_2"]),
            wire_terminal_2=row_dict["wire_terminal_2"],
            aplicator_2=row_dict["aplicator_2"],
            # time=row_dict['time']
        )
        task_pers_obj.save()

    def __sort_allocated_task(self, df, terminals_df, komax_dict, kappas, harnesses, time_dict, shift,
                              type_of_allocaton='parallel'):

        process = ProcessDataframe(df)
        process.filter_availability_komax_terminal(terminals_df)

        amount_dict = {harness.harness.harness_number: 1 for harness in harnesses}

        # alloc_base = process.task_allocation_base(komax_dict, amount_dict, time_dict, hours=shift)
        alloc_base = process.allocate(komax_dict, kappas, amount_dict, time_dict, shift,
                                      type_of_allocation=type_of_allocaton)

        process.delete_word_contain('СВ', 'R')
        first_sort = process.chart.nunique()["wire_terminal_1"] <= process.chart.nunique()["wire_terminal_2"]
        process.sort(method='simple', first_sort=first_sort)

        # alloc = process.task_allocation(komax_dict, amount_dict, time_dict, hours=shift)
        alloc = process.allocate(komax_dict, kappas, amount_dict, time_dict, shift,
                                 type_of_allocation=type_of_allocaton)

        first_sort = not first_sort
        new_process = ProcessDataframe(df)
        new_process.sort(method='simple', first_sort=first_sort)

        # new_alloc = new_process.task_allocation(komax_dict, amount_dict, time_dict, hours=shift)
        new_alloc = new_process.allocate(komax_dict, kappas, amount_dict, time_dict, shift,
                                         type_of_allocation=type_of_allocaton)

        if new_alloc == -1 and alloc == -1:
            final_data = {
                'allocation': [-1, alloc_base],
                'chart': -1
            }
        elif new_alloc == -1:
            final_data = {
                'allocation': [alloc, alloc_base],
                'chart': process.chart
            }
        elif alloc == -1:
            final_data = {
                'allocation': [new_alloc, alloc_base],
                'chart': new_process.new_chart
            }
        else:
            sum_first = sum([i[0] for i in alloc.values()])
            sum_new = sum([i[0] for i in new_alloc.values()])

            if sum_new < sum_first:
                final_data = {
                    'allocation': [new_alloc, alloc_base],
                    'chart': new_process.chart,
                }
            else:
                final_data = {
                    'allocation': [alloc, alloc_base],
                    'chart': process.chart,
                }

        return final_data

    def __get_amount_dict(self, task_name):
        komax_task_query = self.get_komax_task(task_name)
        komax_task = komax_task_query[0]
        komax_task_harnesses = self.get_harnesses(komax_task_obj=komax_task)
        return {harness.harness.harness_number: harness.amount for harness in komax_task_harnesses}

    # TODO: add comparison with base allocation
    def create_allocation(self, task_name):
        """
        allocate
        :param task_name:
        :param type_of_allocation: str, parallel or consistently
        :return:
        """

        task_query = self.get_komax_task(task_name=task_name)
        task_df = 0
        task_obj = 0
        if len(task_query):
            task_obj = task_query[0]
            task_df_query = self.get_task_personal(task_obj=task_query[0])
            if len(task_df_query):
                task_df = read_frame(task_df_query)

        if type(task_df) is int:
            return -1

        task_df.sort_values(
            by=['id'],
            ascending=True,
            inplace=True,
        )

        task_df.index = pd.Index(range(task_df.shape[0]))

        amount_dict = self.__get_amount_dict(task_name)
        """
        sorted_alloc = task_df['allocation'][0]
        alloc_base = alloc_chart_dict['allocation'][1]

        final_alloc = {komax: [1 - round(time/alloc_base[komax], 2)] for komax, time in sorted_alloc.items()}
        """
        final_chart = task_df
        process = ProcessDataframe(final_chart)

        shift = self.get_shift(komax_task_obj=task_obj)
        komaxes_query = self.get_komaxes(komax_task_obj=task_obj)
        komaxes = komaxes_query
        laboriousness_query = self.get_laboriousness()
        laboriousness = laboriousness_query
        komax_dict = self.__get_komaxes_from(read_frame(komaxes))
        time_dict = get_time_from(read_frame(laboriousness))
        kappas = [task_obj.kappas, ]
        type_of_allocation = task_obj.type_of_allocation

        # amount_dict = get_amount_from(read_frame(task_obj.harnesses.all()))

        # alloc = process.task_allocation(komax_dict, quantity=None, time=time_dict, hours=shift)

        alloc = process.allocate(komax_dict, kappas, amount_dict, time_dict, shift, type_of_allocation)

        if type(alloc) is int:
            task_obj.harnesses.all().delete()
            task_obj.komaxes.all().delete()
            task_obj.delete()
            TaskPersonal.objects.filter(komax_task=task_obj).delete()
            return alloc

        komax_task_query = self.get_komax_task(task_name=task_name)
        komax_task = komax_task_query[0]
        komax_task_komaxes = self.get_komaxes(komax_task_obj=komax_task)

        for komax, time in alloc.items():
            alloc[komax] = list(alloc[komax])
            # alloc[komax].append((1 - round(sorted_alloc[komax]/alloc_base[komax])) * 100)
            for komax_time in komax_task_komaxes:
                komax_number = komax_time.komax.number
                if komax_number == komax:
                    komax_time.time = alloc[komax][0]
                    self.save_obj(komax_time)
                    break

            hours = round(alloc[komax][0] // 3600)
            # alloc[komax] = str(hours) + ':' + str(round((final_alloc[komax][0] / 3600 - hours) * 60))
            alloc[komax] = str(hours)

        return alloc
