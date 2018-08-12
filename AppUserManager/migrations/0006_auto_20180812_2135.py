# Generated by Django 2.0.7 on 2018-08-12 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppUserManager', '0005_auto_20180803_1221'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teachers',
            name='EF_FinancialId',
        ),
        migrations.AddField(
            model_name='finances',
            name='EF_TeacherId',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='administrators',
            name='EF_UserStateId',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='chiefcollegeleaders',
            name='EF_UserStateId',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='collegeleaders',
            name='EF_TeacherId',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='collegeleaders',
            name='EF_UserStateId',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='students',
            name='EF_TeacherId',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='students',
            name='EF_TypeId',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='students',
            name='EF_UserStateId',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='superadministrators',
            name='EF_UserStateId',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='teachers',
            name='EF_UserStateId',
            field=models.IntegerField(default=0),
        ),
    ]
