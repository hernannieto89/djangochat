# Generated by Django 2.1.2 on 2018-10-21 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_auto_20181021_0325'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmessage',
            name='room',
            field=models.CharField(default='lobby', max_length=100),
        ),
    ]
