# Generated by Django 2.2.7 on 2020-02-10 22:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmailUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('surname', models.CharField(max_length=128)),
                ('email', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Harness',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateField(auto_now_add=True, verbose_name='created')),
                ('harness_number', models.CharField(max_length=64, unique=True, verbose_name='harness number')),
            ],
        ),
        migrations.CreateModel(
            name='HarnessAmount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.SmallIntegerField()),
                ('harness', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='komax_app.Harness')),
            ],
        ),
        migrations.CreateModel(
            name='Komax',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveSmallIntegerField(unique=True, verbose_name='komaxes')),
                ('identifier', models.CharField(max_length=256)),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'Work'), (2, 'Repair'), (0, 'Not working')], default=1)),
                ('marking', models.PositiveSmallIntegerField(choices=[(2, 'White'), (1, 'Black'), (3, 'Both')], default=1)),
                ('pairing', models.PositiveSmallIntegerField(choices=[(1, 'Yes'), (0, 'No')], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='KomaxTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(max_length=128, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('shift', models.PositiveSmallIntegerField()),
                ('type_of_allocation', models.CharField(max_length=128)),
                ('harnesses', models.ManyToManyField(to='komax_app.HarnessAmount')),
            ],
        ),
        migrations.CreateModel(
            name='Laboriousness',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=256, unique=True)),
                ('time', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Temp_chart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('harness', models.CharField(max_length=128)),
                ('xlsx', models.FileField(upload_to='temp_charts/')),
            ],
        ),
        migrations.CreateModel(
            name='Tickets',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('labels', models.FileField(upload_to='labels/')),
            ],
        ),
        migrations.CreateModel(
            name='TaskPersonal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField()),
                ('notes', models.CharField(max_length=256, null=True)),
                ('marking', models.CharField(max_length=8, null=True)),
                ('wire_type', models.CharField(max_length=8, null=True)),
                ('wire_number', models.CharField(max_length=16, null=True)),
                ('wire_square', models.FloatField(null=True)),
                ('wire_color', models.CharField(max_length=4, null=True)),
                ('wire_length', models.PositiveSmallIntegerField(null=True)),
                ('wire_seal_1', models.CharField(max_length=32, null=True)),
                ('wire_cut_length_1', models.FloatField(null=True)),
                ('wire_terminal_1', models.CharField(max_length=32, null=True)),
                ('aplicator_1', models.CharField(max_length=64, null=True)),
                ('wire_seal_2', models.CharField(max_length=32, null=True)),
                ('wire_cut_length_2', models.FloatField(null=True)),
                ('wire_terminal_2', models.CharField(max_length=32, null=True)),
                ('aplicator_2', models.CharField(max_length=64, null=True)),
                ('harness', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='komax_app.Harness')),
                ('komax', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='komax_app.Komax')),
                ('komax_task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='komax_app.KomaxTask')),
            ],
        ),
        migrations.CreateModel(
            name='KomaxWork',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.PositiveSmallIntegerField()),
                ('komax', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='komax_app.Komax')),
                ('komax_task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='komax_app.KomaxTask')),
            ],
        ),
        migrations.CreateModel(
            name='KomaxTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.IntegerField()),
                ('komax', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='komax_app.Komax')),
            ],
        ),
        migrations.AddField(
            model_name='komaxtask',
            name='komaxes',
            field=models.ManyToManyField(to='komax_app.KomaxTime'),
        ),
        migrations.CreateModel(
            name='HarnessChart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.CharField(max_length=256)),
                ('marking', models.CharField(max_length=8)),
                ('wire_type', models.CharField(max_length=8)),
                ('wire_number', models.CharField(max_length=16)),
                ('wire_square', models.FloatField()),
                ('wire_color', models.CharField(max_length=4)),
                ('wire_length', models.PositiveSmallIntegerField()),
                ('wire_seal_1', models.CharField(max_length=32)),
                ('wire_cut_length_1', models.FloatField()),
                ('wire_terminal_1', models.CharField(max_length=32)),
                ('aplicator_1', models.CharField(max_length=64)),
                ('tube_len_1', models.FloatField()),
                ('armirovka_1', models.CharField(max_length=128)),
                ('wire_seal_2', models.CharField(max_length=32)),
                ('wire_cut_length_2', models.FloatField()),
                ('wire_terminal_2', models.CharField(max_length=32)),
                ('aplicator_2', models.CharField(max_length=64)),
                ('tube_len_2', models.FloatField()),
                ('armirovka_2', models.CharField(max_length=64)),
                ('harness', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='komax_app.Harness')),
            ],
        ),
    ]
