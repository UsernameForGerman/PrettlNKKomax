# Generated by Django 2.2.7 on 2020-03-23 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('komax_app', '0012_auto_20200323_1254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskpersonal',
            name='tube_len_1',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='taskpersonal',
            name='tube_len_2',
            field=models.CharField(max_length=256, null=True),
        ),
    ]
