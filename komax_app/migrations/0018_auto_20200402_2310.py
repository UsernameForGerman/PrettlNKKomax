# Generated by Django 2.2.7 on 2020-04-02 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('komax_app', '0017_auto_20200402_2222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worker',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='worker_images/'),
        ),
    ]
