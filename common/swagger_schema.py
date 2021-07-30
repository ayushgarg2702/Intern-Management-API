from rest_framework.schemas import AutoSchema
import coreapi


class AttendanceStatusSchema(AutoSchema):
    def get_manual_fields(self, path, method):
        extra_field = []
        if method.lower() in ["get"]:
            extra_field = [
                coreapi.Field("UserID"),
            ]
        elif method.lower() in ["post"]:
            extra_field = [
                coreapi.Field("UserID"),
            ]
        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_field


class AttendanceRegisterSchema(AutoSchema):
    def get_manual_fields(self, path, method):
        extra_field = []
        if method.lower() in ["get"]:
            extra_field = [
                coreapi.Field("UserID"),
            ]
        elif method.lower() in ["post"]:
            extra_field = [
                coreapi.Field("UserID"),
            ]
        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_field


class AttendanceClosureSchema(AutoSchema):
    def get_manual_fields(self, path, method):
        extra_field = []
        if method.lower() in ["get"]:
            extra_field = [
                coreapi.Field("UserID"),
            ]
        elif method.lower() in ["post"]:
            extra_field = [
                coreapi.Field("UserID"),
            ]
        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_field


class AttendanceOverallReportSchema(AutoSchema):
    def get_manual_fields(self, path, method):
        extra_field = []
        if method.lower() in ["get"]:
            extra_field = [
                coreapi.Field("UserID"),
            ]
        elif method.lower() in ["post"]:
            extra_field = [
                coreapi.Field("UserID"),
            ]
        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_field


class AttendanceMentorApprovalSchema(AutoSchema):
    def get_manual_fields(self, path, method):
        extra_field = []
        if method.lower() in ["post"]:
            extra_field = [
                coreapi.Field("UserID"),
                coreapi.Field("Mentor"),
                coreapi.Field("ApprovalStatus"),
                coreapi.Field("CreatedOn"),
            ]
        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_field


class AttendancePaginatedLogsSchema(AutoSchema):
    def get_manual_fields(self, path, method):
        extra_field = []
        if method.lower() in ["get"]:
            extra_field = [
                coreapi.Field("UserID"),
                coreapi.Field("PageNumber"),
                coreapi.Field("Size"),
            ]
        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_field


class AttendanceMentorInputSchema(AutoSchema):
    def get_manual_fields(self, path, method):
        extra_field = []
        if method.lower() in ["get"]:
            extra_field = [
                coreapi.Field("Mentor"),
            ]
        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_field


class UserManagementSchema(AutoSchema):
    def get_manual_fields(self, path, method):
        extra_field = []
        if method.lower() in ["get"]:
            extra_field = [
                coreapi.Field("UserID"),
            ]
        elif method.lower() in ["post"]:
            extra_field = [
                coreapi.Field("Role"),
                coreapi.Field("Password"),
                coreapi.Field("FirstName"),
                coreapi.Field("MiddleName"),
                coreapi.Field("LastName"),
                coreapi.Field("ContactNo"),
                coreapi.Field("EmailAddress"),
                coreapi.Field("OrganizationalEmailAddress"),
                coreapi.Field("DateOfJoining"),
                coreapi.Field("Mentor"),
                coreapi.Field("CurrentProject"),
                coreapi.Field("ProjectMentor"),
            ]
        elif method.lower() in ["delete"]:
            extra_field = [
                coreapi.Field("UserID"),
            ]
        elif method.lower() in ["put"]:
            extra_field = [
                coreapi.Field("UserID"),
                coreapi.Field("Role"),
                coreapi.Field("Password"),
                coreapi.Field("FirstName"),
                coreapi.Field("MiddleName"),
                coreapi.Field("LastName"),
                coreapi.Field("ContactNo"),
                coreapi.Field("EmailAddress"),
                coreapi.Field("OrganizationalEmailAddress"),
                coreapi.Field("UserStatus"),
                coreapi.Field("DateOfJoining"),
                coreapi.Field("Mentor"),
                coreapi.Field("CurrentProject"),
                coreapi.Field("ProjectMentor"),
            ]
        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_field

class UserManagementInternsUnderMentorSchema(AutoSchema):
    def get_manual_fields(self, path, method):
        extra_field = []
        if method.lower() in ["get"]:
            extra_field = [
                coreapi.Field("Mentor"),
            ]
        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_field

class BasicAuthenticationLoginSchema(AutoSchema):
    def get_manual_fields(self, path, method):
        extra_field = []
        if method.lower() in ["post"]:
            extra_field = [coreapi.Field("Email"), coreapi.Field("Password")]
        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_field


class SSOAuthenticationLoginSchema(AutoSchema):
    def get_manual_fields(self, path, method):
        extra_field = []
        if method.lower() in ["post"]:
            extra_field = [coreapi.Field("HTTP_LOGINTOKEN")]
        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_field
