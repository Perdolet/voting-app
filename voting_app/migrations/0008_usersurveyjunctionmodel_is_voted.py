# Generated by Django 3.2.9 on 2021-11-04 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting_app', '0007_usersurveyjunctionmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersurveyjunctionmodel',
            name='is_voted',
            field=models.BooleanField(default=False),
        ),
    ]
