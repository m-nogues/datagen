# Generated by Django 2.2 on 2019-04-25 14:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datagen', '0009_auto_20190425_1409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiment',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 25, 19, 24, 19, 812435), verbose_name='end'),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 25, 15, 24, 19, 812410), verbose_name='start'),
        ),
    ]
