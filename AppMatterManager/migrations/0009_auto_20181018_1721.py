# Generated by Django 2.0.8 on 2018-10-18 09:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AppMatterManager', '0008_auto_20181018_1712'),
    ]

    operations = [
        migrations.RenameField(
            model_name='exportmatterdetails',
            old_name='EF_ExportFormId',
            new_name='EF_FormId',
        ),
        migrations.RenameField(
            model_name='importmatterdetails',
            old_name='EF_ImportFormId',
            new_name='EF_FormId',
        ),
        migrations.RenameField(
            model_name='perchasematterdetails',
            old_name='EF_PrePerchaseFormId',
            new_name='EF_FormId',
        ),
    ]
