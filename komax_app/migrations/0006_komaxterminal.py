# Generated by Django 2.2.7 on 2020-02-18 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('komax_app', '0005_auto_20200217_2303'),
    ]

    operations = [
        migrations.CreateModel(
            name='KomaxTerminal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('terminal_name', models.CharField(max_length=64)),
                ('available', models.BooleanField()),
            ],
        ),
    ]
