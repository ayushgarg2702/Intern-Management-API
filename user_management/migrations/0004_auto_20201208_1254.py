# Generated by Django 2.1.15 on 2020-12-08 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0003_auto_20201208_1249'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userroles',
            name='id',
        ),
        migrations.AlterField(
            model_name='userroles',
            name='roleid',
            field=models.CharField(db_column='RoleID', max_length=50, primary_key=True, serialize=False),
        ),
    ]
