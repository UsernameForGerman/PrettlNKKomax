# Generated by Django 3.0.3 on 2020-05-15 11:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('komax_app', '0020_komaxtask_worker'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='komaxtask',
            name='worker',
        ),
    ]
