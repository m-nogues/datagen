# Generated by Django 2.2 on 2019-04-25 13:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datagen', '0007_auto_20190425_1340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='command',
            name='parameters',
            field=models.ManyToManyField(blank=True, to='datagen.Parameter'),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 25, 18, 44, 45, 238600), verbose_name='end'),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 25, 14, 44, 45, 238576), verbose_name='start'),
        ),
        migrations.AlterField(
            model_name='hacker',
            name='actions',
            field=models.ManyToManyField(blank=True, to='datagen.Action'),
        ),
        migrations.AlterField(
            model_name='vm',
            name='actions',
            field=models.ManyToManyField(blank=True, to='datagen.Action'),
        ),
    ]