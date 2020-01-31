# Generated by Django 2.2 on 2019-04-25 13:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datagen', '0006_auto_20190425_1304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiment',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 25, 18, 40, 55, 838433), verbose_name='end'),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 25, 14, 40, 55, 838408), verbose_name='start'),
        ),
        migrations.RemoveField(
            model_name='hacker',
            name='actions',
        ),
        migrations.AddField(
            model_name='hacker',
            name='actions',
            field=models.ManyToManyField(to='datagen.Action'),
        ),
        migrations.RemoveField(
            model_name='hacker',
            name='attacks',
        ),
        migrations.AddField(
            model_name='hacker',
            name='attacks',
            field=models.ManyToManyField(to='datagen.Attack'),
        ),
        migrations.RemoveField(
            model_name='vm',
            name='actions',
        ),
        migrations.AddField(
            model_name='vm',
            name='actions',
            field=models.ManyToManyField(to='datagen.Action'),
        ),
        migrations.RemoveField(
            model_name='vm',
            name='services',
        ),
        migrations.AddField(
            model_name='vm',
            name='services',
            field=models.ManyToManyField(to='datagen.Service'),
        ),
    ]