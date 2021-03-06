# Generated by Django 2.0.8 on 2018-10-19 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppMatterManager', '0009_auto_20181018_1721'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReserveForms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('EF_UserTypeId', models.IntegerField(default=0)),
                ('EF_UserId', models.IntegerField(default=0)),
                ('EF_FormStateId', models.IntegerField(default=0)),
                ('EF_Time', models.DateTimeField(default=0)),
                ('EF_CensorePatternId', models.IntegerField(default=0)),
                ('EF_UserId1', models.IntegerField(default=0)),
                ('EF_CensoreStateId1', models.IntegerField(default=0)),
                ('EF_CensoreComment1', models.CharField(default='', max_length=255)),
                ('EF_UserId2', models.IntegerField(default=0)),
                ('EF_CensoreStateId2', models.IntegerField(default=0)),
                ('EF_CensoreComment2', models.CharField(default='', max_length=255)),
                ('EF_UserId3', models.IntegerField(default=0)),
                ('EF_CensoreStateId3', models.IntegerField(default=0)),
                ('EF_CensoreComment3', models.CharField(default='', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ReserveMatterDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('EF_FormId', models.IntegerField(default=0)),
                ('EF_MatterId', models.IntegerField(default=0)),
                ('EF_MatterCount', models.IntegerField(default=0)),
            ],
        ),
    ]
