# Generated by Django 3.0 on 2020-06-02 06:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('komax_app', '0024_auto_20200528_0855'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worker',
            name='current_komax',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='komax_app.Komax'),
        ),
    ]
