# Generated by Django 2.1.15 on 2020-12-10 09:07

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userattendancelogs',
            name='approvalstatusdate',
            field=models.DateField(db_column='ApprovalStatusDate', default=datetime.datetime(2020, 12, 10, 9, 7, 36, 194216, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='userattendancelogs',
            name='checkin',
            field=models.DateTimeField(db_column='CheckIn', default=datetime.datetime(2020, 12, 10, 9, 7, 36, 194216, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='userattendancelogs',
            name='createdon',
            field=models.DateField(db_column='CreatedOn', default=datetime.datetime(2020, 12, 10, 9, 7, 36, 194216, tzinfo=utc)),
        ),
    ]
