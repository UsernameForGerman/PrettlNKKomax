# Generated by Django 2.2.7 on 2020-04-06 22:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('komax_app', '0018_auto_20200402_2310'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskpersonal',
            name='worker',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='komax_app.Worker'),
        ),
        migrations.CreateModel(
            name='KomaxStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('komax', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='komax_app.Komax')),
                ('task_personal', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='komax_app.TaskPersonal')),
            ],
        ),
    ]
