from django.db import models
from django.utils import timezone
import uuid

def increment_role_id():
    last_role = UserDetails.objects.all().order_by('userid').last()
    if not last_role:
        return 'CL' + '0001'
    role_id = last_role.userid
    role_int = int(role_id[2:])
    new_role_int = role_int + 1
    new_role_id = 'CL' + str(new_role_int).zfill(4)
    return new_role_id

class UserDetails(models.Model):
    userid = models.CharField(
        db_column="UserID", primary_key=True, unique=True, max_length=50,default= increment_role_id
    )
    userstatus=models.CharField(db_column="UserStatus", max_length=50, default="Enable")
    role = models.CharField(db_column="Role", max_length=50, default="Intern")
    dateofjoining = models.DateTimeField(db_column="JoiningDate", default=timezone.now,null=True)
    mentor = models.CharField(db_column="Mentor", max_length=50,null=True)
    currentproject = models.CharField(db_column="CurrentProject", max_length=50,null=True)
    projectmentor = models.CharField(db_column="ProjectMentor", max_length=50,null=True)
    password = models.CharField(db_column="Password", max_length=50, default="user")
    firstname = models.CharField(db_column="FirstName", max_length=50)
    middlename = models.CharField(
        db_column="MiddleName", max_length=50, null=True
    )
    lastname = models.CharField(db_column="LastName", max_length=50)
    contactno = models.CharField(
        db_column="ContactNo", max_length=20, null=True
    )
    emailaddress = models.CharField(
        db_column="EmailAddress", unique=True, max_length=100
    )
    organizationemailaddress= models.CharField(
        db_column="OrganizationEmailAddress", unique=False, max_length=100, null=True
    )
    createddate = models.DateTimeField(db_column="CreatedDate", default=timezone.now)

    class Meta:
        managed = True
        db_table = "UserDetails"

    def __str__(self):
        return (self.firstname+" "+self.lastname)

class UserRoles(models.Model):
    roleid=models.CharField(db_column="RoleID",primary_key=True, max_length=50 )
    rolename=models.CharField(db_column="RoleName", max_length=50)
    createddate = models.DateTimeField(db_column="CreatedOn", default=timezone.now)
    class Meta:
        managed = True
        db_table = "UserRoles"

