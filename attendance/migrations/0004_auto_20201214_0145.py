# Generated by Django 2.1.15 on 2020-12-14 01:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0003_auto_20201214_0140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userattendancelogs',
            name='approvalstatusdate',
            field=models.DateField(db_column='ApprovalStatusDate', default=datetime.datetime(2020, 12, 14, 1, 45, 4, 887997)),
        ),
        migrations.AlterField(
            model_name='userattendancelogs',
            name='checkin',
            field=models.DateTimeField(db_column='CheckIn', default=datetime.datetime(2020, 12, 14, 1, 45, 4, 886996)),
        ),
        migrations.AlterField(
            model_name='userattendancelogs',
            name='createdon',
            field=models.DateField(db_column='CreatedOn', default=datetime.datetime(2020, 12, 14, 1, 45, 4, 887997)),
        ),
    ]
