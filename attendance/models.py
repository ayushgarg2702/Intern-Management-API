from django.db import models
from django.utils import timezone
import uuid

# Create your models here.
class UserAttendanceLogs(models.Model):
    logid = models.UUIDField(db_column="LogID",primary_key=True, default=uuid.uuid4, editable=False)
    userid = models.CharField(db_column="UserID", max_length=20, null=True)
    checkin = models.DateTimeField(db_column="CheckIn", default=timezone.now())
    checkout = models.DateTimeField(db_column="CheckOut", null=True)
    approvalstatus = models.CharField(
        db_column="ApprovalStatus", max_length=50, default="Pending"
    )
    approvalstatusdate = models.DateField(db_column="ApprovalStatusDate", default=timezone.now())
    createdon = models.DateField(db_column="CreatedOn", default=timezone.now())

    class Meta:
        managed = True
        db_table = "UserAttendanceLogs"
