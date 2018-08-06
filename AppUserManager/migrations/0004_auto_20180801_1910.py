# Generated by Django 2.0.7 on 2018-08-01 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppUserManager', '0003_auto_20180801_1153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='administrators',
            name='EF_OfficeAddress',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='administrators',
            name='EF_PhoneNum',
            field=models.CharField(default='', max_length=15),
        ),
        migrations.AlterField(
            model_name='administrators',
            name='EF_UserName',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='administrators',
            name='EF_UserStateId',
            field=models.IntegerField(default='1'),
        ),
        migrations.AlterField(
            model_name='chiefcollegeleaders',
            name='EF_OfficeAddress',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='chiefcollegeleaders',
            name='EF_PhoneNum',
            field=models.CharField(default='', max_length=15),
        ),
        migrations.AlterField(
            model_name='chiefcollegeleaders',
            name='EF_TeacherId',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='chiefcollegeleaders',
            name='EF_UserName',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='collegeleaders',
            name='EF_OfficeAddress',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='collegeleaders',
            name='EF_PhoneNum',
            field=models.CharField(default='', max_length=15),
        ),
        migrations.AlterField(
            model_name='collegeleaders',
            name='EF_TeacherId',
            field=models.IntegerField(default='0'),
        ),
        migrations.AlterField(
            model_name='collegeleaders',
            name='EF_UserName',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='collegeleaders',
            name='EF_UserStateId',
            field=models.IntegerField(default='1'),
        ),
        migrations.AlterField(
            model_name='finances',
            name='EF_Name',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='finances',
            name='EF_TotalAmount',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='students',
            name='EF_TeacherId',
            field=models.IntegerField(default='0'),
        ),
        migrations.AlterField(
            model_name='students',
            name='EF_TypeId',
            field=models.IntegerField(default='0'),
        ),
        migrations.AlterField(
            model_name='students',
            name='EF_UserName',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='studenttypes',
            name='EF_TypeName',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='superadministrators',
            name='EF_OfficeAddress',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='superadministrators',
            name='EF_PhoneNum',
            field=models.CharField(default='', max_length=15),
        ),
        migrations.AlterField(
            model_name='superadministrators',
            name='EF_UserName',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='teachers',
            name='EF_FinancialId',
            field=models.IntegerField(default='0'),
        ),
        migrations.AlterField(
            model_name='teachers',
            name='EF_OfficeAddress',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='teachers',
            name='EF_PhoneNum',
            field=models.CharField(default='', max_length=15),
        ),
        migrations.AlterField(
            model_name='teachers',
            name='EF_UserName',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='userstates',
            name='EF_TypeName',
            field=models.CharField(default='离线', max_length=30),
        ),
        migrations.AlterField(
            model_name='usertypes',
            name='EF_TypeName',
            field=models.CharField(default='', max_length=30),
        ),
    ]
