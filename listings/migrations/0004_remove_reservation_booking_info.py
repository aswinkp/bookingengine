# Generated by Django 3.2 on 2021-05-24 07:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0003_auto_20210524_0725'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='booking_info',
        ),
    ]
