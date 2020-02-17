from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404
import datetime


class Harness(models.Model):
    created = models.DateField(verbose_name=_('created'), auto_now_add=True)
    harness_number = models.CharField(max_length=64, unique=True, verbose_name=_('harness number'))

    def __str__(self):
        return self.harness_number

class HarnessChart(models.Model):
    harness = models.ForeignKey(Harness, on_delete=models.CASCADE)
    notes = models.CharField(max_length=256)
    marking = models.CharField(max_length=8)
    wire_type = models.CharField(max_length=8)
    wire_number = models.CharField(max_length=16)
    wire_square = models.FloatField()
    wire_color = models.CharField(max_length=4)
    wire_length = models.PositiveSmallIntegerField()
    wire_seal_1 = models.CharField(max_length=32)
    wire_cut_length_1 = models.FloatField()
    wire_terminal_1 = models.CharField(max_length=32)
    aplicator_1 = models.CharField(max_length=64)
    tube_len_1 = models.FloatField()
    armirovka_1 = models.CharField(max_length=128)
    wire_seal_2 = models.CharField(max_length=32)
    wire_cut_length_2 = models.FloatField()
    wire_terminal_2 = models.CharField(max_length=32)
    aplicator_2 = models.CharField(max_length=64)
    tube_len_2 = models.FloatField()
    armirovka_2 = models.CharField(max_length=64)

    def __str__(self):
        return self.harness.harness_number

    def save_from_dataframe(self, harness_dataframe, harness_number):
        for row in harness_dataframe.iterrows():
            row_dict = row[1]
            HarnessChart(
                harness=get_object_or_404(Harness, harness_number=harness_number),
                notes=row_dict["Примечание"],
                marking=row_dict["Маркировка"],
                wire_type=row_dict["Вид провода"],
                wire_number=row_dict["№ провода"],
                wire_square=float(row_dict["Сечение"]),
                wire_color=row_dict["Цвет"],
                wire_length=int(row_dict["Длина, мм (± 3мм)"]),
                wire_seal_1=row_dict["Уплотнитель 1"],
                wire_cut_length_1=float(row_dict["Частичное снятие 1"]),
                wire_terminal_1=row_dict["Наконечник 1"],
                aplicator_1=row_dict["Аппликатор 1"],
                tube_len_1=float(row_dict["Длина трубки, L (мм) 1"]),
                armirovka_1=row_dict["Армировка 1 (Трубка ПВХ, Тр.Терм., изоляторы)"],
                wire_seal_2=row_dict["Уплотнитель 2"],
                wire_cut_length_2=float(row_dict["Частичное снятие 2"]),
                wire_terminal_2=row_dict["Наконечник 2"],
                aplicator_2=row_dict["Аппликатор 2"],
                tube_len_2=float(row_dict["Длина трубки, L (мм) 2"]),
                armirovka_2=row_dict["Армировка 2 (Трубка ПВХ, Тр.Терм., изоляторы)"]
            ).save()

            """except:
                error_harnesses = get_object_or_404(Harness, harness_number=harness_number)
                try:
                    error_harnesses.delete()
                except:
                    pass"""

class Temp_chart(models.Model):
    harness = models.CharField(max_length=128)
    xlsx = models.FileField(upload_to='temp_charts/')

    def __str__(self):
        return self.harness

class Kappa(models.Model):
    STATUS_CHOICES = [
        (1, 'Work'),
        (2, 'Repair'),
        (0, 'Not working')
    ]

    number = models.PositiveSmallIntegerField(unique=True, verbose_name=_('kappa'))
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)

    def __str__(self):
        return str(self.number)

class Komax(models.Model):
    STATUS_CHOICES = [
        (1, 'Work'),
        (2, 'Repair'),
        (0, 'Not working')
    ]
    MARKING_CHOICES = [
        (2, 'White'),
        (1, 'Black'),
        (3, 'Both')
    ]
    PAIRING_CHOICES = [
        (1, 'Yes'),
        (0, 'No')
    ]

    number = models.PositiveSmallIntegerField(unique=True, verbose_name=_('komaxes'))
    identifier = models.CharField(max_length=256)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)
    marking = models.PositiveSmallIntegerField(choices=MARKING_CHOICES, default=1)
    pairing = models.PositiveSmallIntegerField(choices=PAIRING_CHOICES, default=0)
    group_of_square = models.CharField(max_length=6)

    def __str__(self):
        return str(self.number)

class Laboriousness(models.Model):
    action = models.CharField(max_length=256, unique=True)
    time = models.FloatField()

    def __str__(self):
        return self.action

class HarnessAmount(models.Model):
    harness = models.ForeignKey(Harness, on_delete=models.CASCADE)
    amount = models.SmallIntegerField()

    def __str__(self):
        return self.harness.harness_number

class KomaxTime(models.Model):
    komax = models.ForeignKey(Komax, on_delete=models.CASCADE)
    time = models.IntegerField()

    def __str__(self):
        return  str(self.komax.number) + ' : ' + str(self.time)

class KomaxTask(models.Model):
    task_name = models.CharField(max_length=128, unique=True)
    created = models.DateTimeField(verbose_name=_('created'), auto_now_add=True)
    harnesses = models.ManyToManyField(HarnessAmount)
    komaxes = models.ManyToManyField(KomaxTime)
    kappas = models.ForeignKey(Kappa, on_delete=models.CASCADE)
    shift = models.PositiveSmallIntegerField()
    type_of_allocation = models.CharField(max_length=128)

    def __str__(self):
        return self.task_name

class TaskPersonal(models.Model):
    komax_task = models.ForeignKey(KomaxTask, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField()
    harness = models.ForeignKey(Harness, on_delete=models.CASCADE)
    komax = models.ForeignKey(Komax, on_delete=models.CASCADE)
    notes = models.CharField(max_length=256, null=True)
    marking = models.CharField(max_length=8, null=True)
    wire_type = models.CharField(max_length=8, null=True)
    wire_number = models.CharField(max_length=16, null=True)
    wire_square = models.FloatField(null=True)
    wire_color = models.CharField(max_length=4, null=True)
    wire_length = models.PositiveSmallIntegerField(null=True)
    wire_seal_1 = models.CharField(max_length=32, null=True)
    wire_cut_length_1 = models.FloatField(null=True)
    wire_terminal_1 = models.CharField(max_length=32, null=True)
    aplicator_1 = models.CharField(max_length=64, null=True)
    wire_seal_2 = models.CharField(max_length=32, null=True)
    wire_cut_length_2 = models.FloatField(null=True)
    wire_terminal_2 = models.CharField(max_length=32, null=True)
    aplicator_2 = models.CharField(max_length=64, null=True)

    def save_from_df(self, row_dict, komax_task, harness_obj, komax_obj):
        return

    def __str__(self):
        return self.task.task_name

def komax_number_harness_number_path(instance, komax_number, harness_number):
    return '{}-{}'.format(komax_number, harness_number)

class Tickets(models.Model):
    name = models.CharField(max_length=128)
    labels = models.FileField(upload_to='labels/')

    def __str__(self):
        return self.name

class KomaxWork(models.Model):
    komax_task = models.ForeignKey(KomaxTask, on_delete=models.CASCADE)
    komax = models.ForeignKey(Komax, on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.komax_task

class EmailUser(models.Model):
    name = models.CharField(max_length=128)
    surname = models.CharField(max_length=128)
    email = models.CharField(max_length=128)

    def __str__(self):
        return self.email
