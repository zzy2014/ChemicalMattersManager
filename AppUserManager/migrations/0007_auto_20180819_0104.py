# Generated by Django 2.0.7 on 2018-08-18 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppUserManager', '0006_auto_20180812_2135'),
    ]

    operations = [
        migrations.AddField(
            model_name='students',
            name='EF_OfficeAddress',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='students',
            name='EF_PhoneNum',
            field=models.CharField(default='', max_length=15),
        ),
    ]
