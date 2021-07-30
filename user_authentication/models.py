from django.db import models
from django.utils import timezone


class UserAuthenticationLogs(models.Model):
    userid = models.CharField(
        db_column="UserID", primary_key=True, unique=True, max_length=50
    )
    password = models.CharField(db_column="Password", max_length=50, default="user")
    contactno = models.CharField(
        db_column="ContactNo", max_length=20, null=True
    )
    emailaddress = models.CharField(
        db_column="EmailAddress", unique=True, max_length=100
    )
    organizationemailaddress = models.CharField(
        db_column="OrganizationEmailAddress", unique=True, max_length=100, null=True
    )
    logintime = models.DateTimeField(db_column="LoginTime", default=timezone.now)

    class Meta:
        managed = True
        db_table = "UserAuthenticationLogs"
