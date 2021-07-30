from django.urls import path
from . import views


urlpatterns = [
    path("api/CurrentStatus", views.AttendanceStatus.as_view()),
    path("api/AttendanceRegistration", views.AttendanceRegister.as_view()),
    path("api/AttendanceClosure", views.AttendanceClosure.as_view()),
    path("api/AttendanceReport", views.AttendancePaginatedLogs.as_view()),
    path("api/AttendanceReportTotal", views.AttendanceOverallReport.as_view()),
    path("api/AttendanceApprovalStatus", views.AttendanceApprovalStatus.as_view()),
    path("api/AttendanceMentorApproval", views.AttendanceMentorApproval.as_view()),
]