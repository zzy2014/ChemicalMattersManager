# Generated by Django 2.0.7 on 2018-09-04 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CensorePatterns',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('EF_StepsCount', models.IntegerField(default=0)),
                ('EF_UserTypeId1', models.IntegerField(default=0)),
                ('EF_UserTypeId2', models.IntegerField(default=0)),
                ('EF_UserTypeId3', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='CensoreStates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('EF_States', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='FormStates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('EF_StateName', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='ImportForms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('EF_UserId', models.IntegerField(default=0)),
                ('EF_FormStateId', models.IntegerField(default=0)),
                ('EF_MatterDetailId', models.IntegerField(default=0)),
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
            name='MatterDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('EF_ImportMatterId', models.IntegerField(default=0)),
                ('EF_MatterId', models.IntegerField(default=0)),
                ('EF_MatterCount', models.IntegerField(default=0)),
            ],
        ),
    ]