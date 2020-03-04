# Generated by Django 2.2.7 on 2020-03-03 15:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('komax_app', '0007_auto_20200218_2232'),
    ]

    operations = [
        migrations.CreateModel(
            name='KomaxOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Requested', 'Requested'), ('Received', 'Received')], max_length=32, null=True)),
                ('komax', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='komax_app.Komax')),
            ],
        ),
        migrations.AddField(
            model_name='komaxtask',
            name='loading_type',
            field=models.CharField(choices=[('New', 'New'), ('Mix', 'Mix'), ('Urgent', 'Urgent')], default='New', max_length=64),
        ),
        migrations.AddField(
            model_name='taskpersonal',
            name='loaded',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='taskpersonal',
            name='time',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='komaxtask',
            name='type_of_allocation',
            field=models.CharField(choices=[('Parallel', 'Parallel'), ('Consistently', 'Consistently')], default='Parallel', max_length=128),
        ),
        migrations.CreateModel(
            name='KomaxTaskPersonal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField()),
                ('notes', models.CharField(max_length=256, null=True)),
                ('marking', models.CharField(max_length=8, null=True)),
                ('wire_type', models.CharField(max_length=128, null=True)),
                ('wire_number', models.CharField(max_length=16, null=True)),
                ('wire_square', models.FloatField(null=True)),
                ('wire_color', models.CharField(max_length=8, null=True)),
                ('wire_length', models.PositiveSmallIntegerField(null=True)),
                ('wire_seal_1', models.CharField(max_length=32, null=True)),
                ('wire_cut_length_1', models.FloatField(null=True)),
                ('wire_terminal_1', models.CharField(max_length=32, null=True)),
                ('aplicator_1', models.CharField(max_length=64, null=True)),
                ('wire_seal_2', models.CharField(max_length=32, null=True)),
                ('wire_cut_length_2', models.FloatField(null=True)),
                ('wire_terminal_2', models.CharField(max_length=32, null=True)),
                ('aplicator_2', models.CharField(max_length=64, null=True)),
                ('time', models.IntegerField(null=True)),
                ('harness', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='komax_app.Harness')),
                ('kappa', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='komax_app.Kappa')),
                ('komax', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='komax_app.Komax')),
                ('komax_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='komax_app.KomaxOrder')),
                ('komax_task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='komax_app.KomaxTask')),
            ],
        ),
        migrations.AddField(
            model_name='komaxorder',
            name='komax_task',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='komax_app.KomaxTask'),
        ),
    ]
