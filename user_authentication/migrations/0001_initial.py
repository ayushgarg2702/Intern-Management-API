# Generated by Django 2.1.15 on 2020-12-05 12:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserAuthenticationLogs',
            fields=[
                ('userid', models.CharField(db_column='UserID', max_length=50, primary_key=True, serialize=False, unique=True)),
                ('password', models.CharField(db_column='Password', default='user', max_length=50)),
                ('contactno', models.CharField(blank=True, db_column='ContactNo', max_length=20, null=True)),
                ('emailaddress', models.CharField(db_column='EmailAddress', max_length=100, unique=True)),
                ('organizationemailaddress', models.CharField(blank=True, db_column='OrganizationEmailAddress', max_length=100, unique=True)),
                ('logintime', models.DateTimeField(db_column='LoginTime', default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'UserAuthenticationLogs',
                'managed': True,
            },
        ),
    ]
