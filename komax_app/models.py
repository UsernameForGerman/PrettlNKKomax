from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
#from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
import os
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime
from django.urls import reverse
from django.http import Http404
import traceback


User = get_user_model()


"""
@receiver(post_save, sender=User)
def create_user_worker(sender, instance, created, **kwargs):
    if created:
        Worker.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_worker(sender, instance, **kwargs):
    instance.worker.save()
"""
class Harness(models.Model):
    created = models.DateField(verbose_name=_('created'), auto_now_add=True)
    harness_number = models.CharField(max_length=64, unique=True, verbose_name=_('harness number'))

    def __str__(self):
        return self.harness_number

class HarnessChart(models.Model):
    harness = models.ForeignKey(Harness, on_delete=models.CASCADE)
    notes = models.CharField(max_length=256, null=True)
    marking = models.CharField(max_length=8)
    wire_type = models.CharField(max_length=128)
    wire_number = models.CharField(max_length=16)
    wire_square = models.FloatField()
    wire_color = models.CharField(max_length=8)
    wire_length = models.PositiveSmallIntegerField()

    armirovka_1 = models.CharField(max_length=128, null=True)
    tube_len_1 = models.CharField(max_length=256, null=True)
    wire_seal_1 = models.CharField(max_length=32, null=True)
    wire_cut_length_1 = models.FloatField()
    wire_terminal_1 = models.CharField(max_length=32, null=True)
    aplicator_1 = models.CharField(max_length=64, null=True)

    armirovka_2 = models.CharField(max_length=128, null=True)
    tube_len_2 = models.CharField(max_length=256, null=True)
    wire_seal_2 = models.CharField(max_length=32, null=True)
    wire_cut_length_2 = models.FloatField()
    wire_terminal_2 = models.CharField(max_length=32, null=True)
    aplicator_2 = models.CharField(max_length=64, null=True)



    def __str__(self):
        return self.harness.harness_number

    @classmethod
    def save_from_dataframe(self, harness_dataframe, harness_number):
        old_harness_charts = self.objects.filter(harness__harness_number__iexact=harness_number)
        if len(old_harness_charts):
            old_harness_charts.delete()

        new_harness_charts = list()
        harness = get_object_or_404(Harness, harness_number=harness_number)
        for row in harness_dataframe.iterrows():
            row_dict = row[1]
            try:
                new_harness_charts.append(
                    self(
                        harness=harness,
                        notes=row_dict["Примечание"],
                        marking=str(row_dict["Маркировка"]),
                        wire_type=str(row_dict["Вид провода"]),
                        wire_number=str(row_dict["№ провода"]),
                        wire_square=float(row_dict["Сечение"]),
                        wire_color=str(row_dict["Цвет"]),
                        wire_length=int(row_dict["Длина, мм (± 3мм)"]),
                        wire_seal_1=str(row_dict["Уплотнитель 1"]),
                        wire_cut_length_1=float(row_dict["Частичное снятие 1"]),
                        wire_terminal_1=str(row_dict["Наконечник 1"]),
                        aplicator_1=str(row_dict["Аппликатор 1"]),
                        tube_len_1=str(row_dict["Длина трубки, L (мм) 1"]),
                        armirovka_1=str(row_dict["Армировка 1 (Трубка ПВХ, Тр. Терм., изоляторы)"]),
                        wire_seal_2=str(row_dict["Уплотнитель 2"]),
                        wire_cut_length_2=float(row_dict["Частичное снятие 2"]),
                        wire_terminal_2=str(row_dict["Наконечник 2"]),
                        aplicator_2=str(row_dict["Аппликатор 2"]),
                        tube_len_2=str(row_dict["Длина трубки, L (мм) 2"]),
                        armirovka_2=str(row_dict["Армировка 2 (Трубка ПВХ, Тр. Терм., изоляторы)"])
                    )
                )
            except Exception as e:
                harness.delete()
                raise Http404(traceback.format_exc())

        self.objects.bulk_create(new_harness_charts)

class Temp_chart(models.Model):
    harness = models.CharField(max_length=128)
    xlsx = models.FileField(upload_to='temp_charts/')

    def __str__(self):
        return self.harness

class KomaxTerminal(models.Model):
    terminal_name = models.CharField(max_length=64, unique=True)
    terminal_available = models.BooleanField(default=True)
    seal_installed = models.BooleanField(default=True)

    def __str__(self):
        return self.terminal_name + str(self.terminal_available) + str(self.seal_installed)

class KomaxSeal(models.Model):
    seal_name = models.CharField(max_length=64, unique=True)
    seal_available = models.BooleanField(default=True)

    def __str__(self):
        return self.seal_name + str(self.seal_available)

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
    def get_absolute_url(self):
        return reverse('komax_app:laboriousness')

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

class Worker(models.Model):
    LOCALE_CHOICES = [
        (1, 'ru'),
        (2, 'en')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, db_index=True)
    image = models.ImageField(
        upload_to='worker_images/',
        null=True,
        blank=True,
        editable=True,
    )
    current_komax = models.ForeignKey(Komax, on_delete=models.SET_NULL, blank=True, null=True)
    locale = models.SmallIntegerField('language', choices=LOCALE_CHOICES, default=1)


    def save(self, *args, **kwargs):
        workers = Worker.objects.filter(id=self.id)
        old_path = None
        if len(workers):
            image = workers.first().image
            # image = Worker.objects.get(id=self.id).image

            if bool(image):
                old_path = image.url
                print(os.path.exists(old_path))
                if os.path.exists(old_path):
                    os.remove(image.url)

        if bool(self.image):
            image = Image.open(self.image)
            image_format = self.image.name.split('.')[-1]
            image_name = self.image.name.split('.')[0]

            output = BytesIO()

            image = image.resize((200, 200))
            if image_format == 'png':
                image.save(output, format='PNG', quality=100)
            else:
                image.save(output, format='JPEG', quality=100)
            output.seek(0)

            self.image = InMemoryUploadedFile(output, 'ImageField', '{name}.{format}'.format(name=image_name, format=image_format), 'image/jpeg', sys.getsizeof(output), None)

            if old_path is not None and os.path.exists(old_path):
                os.remove(old_path)
        super(Worker, self).save(*args, **kwargs)


    def __str__(self):
        return "{} - {}".format(self.user, self.current_komax)

class KomaxTask(models.Model):
    LOADING_TYPES = [
        ('New', 'New'),
        ('Mix', 'Mix'),
        ('Urgent', 'Urgent')
    ]

    ALLOCATION_TYPES = [
        ('Parallel', 'Parallel'),
        ('Consistently', 'Consistently'),
    ]

    STATUS_TYPES = [
        (1, 'Created'),
        (2, 'Ordered'),
        (3, 'Loaded'),
        (4, 'Done')
    ]

    task_name = models.CharField(max_length=128, unique=True)
    created = models.DateTimeField(verbose_name=_('created'), auto_now_add=True)
    harnesses = models.ManyToManyField(HarnessAmount)
    komaxes = models.ManyToManyField(KomaxTime)
    kappas = models.ForeignKey(Kappa, on_delete=models.CASCADE, null=True)
    shift = models.PositiveSmallIntegerField()
    type_of_allocation = models.CharField(default='Parallel', max_length=128, choices=ALLOCATION_TYPES)
    loading_type = models.CharField(default='New', max_length=64, choices=LOADING_TYPES)
    status = models.SmallIntegerField(choices=STATUS_TYPES, default=1)
    # worker = models.ForeignKey(Worker,on_delete=models.CASCADE, null=True)
    # ordered = models.BooleanField(default=False)
    # loaded = models.BooleanField(default=False)

    def __str__(self):
        return self.task_name

class OrderedKomaxTask(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In progress', 'In progress'),
        ('Finished', 'Finished'),
    ]

    komax_task = models.ForeignKey(KomaxTask, on_delete=models.CASCADE)
    komax = models.ForeignKey(KomaxTime, on_delete=models.CASCADE)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=64, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return str(self.komax_task) + ' - ' + str(self.worker) + ' - ' + self.status

class KomaxOrder(models.Model):
    STATUS_CHOICES = [
        ('Requested', 'Requested'),
        ('Received', 'Received')
    ]

    komax_task = models.ForeignKey(KomaxTask, on_delete=models.CASCADE, null=True)
    komax = models.ForeignKey(Komax, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, null=True)


    def __str__(self):
        return self.komax_task.task_name + ' '

class TaskPersonal(models.Model):
    komax_task = models.ForeignKey(KomaxTask, on_delete=models.CASCADE)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, null=True, related_name='task_personal')
    amount = models.PositiveSmallIntegerField()
    harness = models.ForeignKey(Harness, on_delete=models.CASCADE)
    komax = models.ForeignKey(Komax, on_delete=models.CASCADE, null=True)
    kappa = models.ForeignKey(Kappa, on_delete=models.CASCADE, null=True)
    notes = models.CharField(max_length=256, null=True)
    marking = models.CharField(max_length=8, null=True)
    wire_type = models.CharField(max_length=128, null=True)
    wire_number = models.CharField(max_length=16, null=True)
    wire_square = models.FloatField(null=True)
    wire_color = models.CharField(max_length=8, null=True)
    wire_length = models.PositiveSmallIntegerField(null=True)

    tube_len_1 = models.CharField(max_length=256, null=True)
    wire_seal_1 = models.CharField(max_length=32, null=True)
    wire_cut_length_1 = models.FloatField(null=True)
    wire_terminal_1 = models.CharField(max_length=32, null=True)
    aplicator_1 = models.CharField(max_length=64, null=True)

    tube_len_2 = models.CharField(max_length=256, null=True)
    wire_seal_2 = models.CharField(max_length=32, null=True)
    wire_cut_length_2 = models.FloatField(null=True)
    wire_terminal_2 = models.CharField(max_length=32, null=True)
    aplicator_2 = models.CharField(max_length=64, null=True)

    time = models.IntegerField(null=True)
    loaded = models.BooleanField(default=False)

    def save_from_df(self, row_dict, komax_task, harness_obj, komax_obj):
        return

    def __str__(self):
        return "{} - {} - {}".format(self.komax_task.task_name, self.harness.harness_number, self.komax.number)

class KomaxStatus(models.Model):
    komax = models.ForeignKey(Komax, unique=True, on_delete=models.CASCADE)
    task_personal = models.ForeignKey(TaskPersonal, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.komax.number)

class KomaxTaskCompletion(models.Model):
    timestamp = models.TimeField('Time last updated', auto_now=True)
    komax_task = models.ForeignKey(KomaxTask, on_delete=models.CASCADE, unique=True)
    harness = models.ForeignKey(Harness, on_delete=models.CASCADE)
    left_time = models.PositiveIntegerField('Time left to create harness')
    percent_completion = models.PositiveSmallIntegerField('Percent completion harness')

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



