# Generated by Django 3.2.9 on 2021-11-03 22:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveymodel',
            name='finishing_date',
            field=models.DateField(default=datetime.datetime(2021, 11, 5, 22, 45, 22, 531136)),
        ),
    ]
