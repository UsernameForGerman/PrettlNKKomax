# Generated by Django 2.2.7 on 2020-03-19 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('komax_app', '0010_auto_20200319_2146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='harnesschart',
            name='armirovka_2',
            field=models.CharField(max_length=128, null=True),
        ),
    ]
