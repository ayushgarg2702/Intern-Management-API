from datetime import timedelta, datetime, date
import json
from math import ceil

from rest_framework.views import APIView
from rest_framework.request import Request
from django.http.response import JsonResponse, HttpResponse
from django.core.serializers import serialize
from django.utils import timezone

from .models import UserAttendanceLogs as UserAttendanceLogsModel
from .sqlqueries import StoredProcedure, Queries
from user_management.models import UserDetails as UserDetailsModel
from common.read_logger import LoggerSetup
from common.create_response import create_failure, create_success
from common.swagger_schema import (
    AttendanceStatusSchema,
    AttendanceRegisterSchema,
    AttendanceClosureSchema,
    AttendanceOverallReportSchema,
    AttendancePaginatedLogsSchema,
    AttendanceMentorInputSchema,
    AttendanceMentorApprovalSchema,
)


class AttendanceStatus(APIView):
    schema = AttendanceStatusSchema()

    def __init__(self):
        self.logger = LoggerSetup(loggerName=str(__file__)).getLogger()
        print("helloworld")

    def get(self, request: Request) -> JsonResponse:
        """
        Attendance Current Status
        #### AttendanceStatus API

        #### Request Method
            GET

        #### Response parameter
        | Field name | Meaning | Types of |
        |:------:|:------:|:------:|
        | Message | message | String |
        | ReplyCode | code | String |
        | Data | List Of Datapoints | JSON |

        #### Response format
            JSON

        #### Response example
            {"Message": "Success", "ReplyCode": "Success" , "Data": {}}
        """
        try:
            userid = request.query_params["UserID"]
        except Exception as e:
            self.logger.error("Error in Attendance API - Request Payload : " + str(e))
            return JsonResponse(
                create_failure("Error in Request Payload", "Fail"), status=400
            )
        try:
            try:
                user = UserDetailsModel.objects.get(userid=userid)
            except Exception as e:
                self.logger.error("Error while fetching user")
                return JsonResponse(
                    create_failure("Error while fetching user", "Fail"), status=400
                )
            try:
                user_attendance_data = UserAttendanceLogsModel.objects.get(
                    userid=userid, createdon=timezone.now().date()
                )
            except Exception as e:
                response = {
                    "Status": "NotCheckedIn",
                    "CheckInTime": None,
                    "CheckOutTime": None,
                }
                return JsonResponse(create_success("User Not Logged In", response))
            print(user_attendance_data.checkout)
            if user_attendance_data.checkout is None:
                response = {
                    "Status": "CheckedIn",
                    "CheckInTime": user_attendance_data.checkin,
                    "CheckOutTime": user_attendance_data.checkout,
                }
                return JsonResponse(create_success("User has checked in", response))
            else:
                response = {
                    "Status": "CheckedOut",
                    "CheckInTime": user_attendance_data.checkin,
                    "CheckOutTime": user_attendance_data.checkout,
                }
                return JsonResponse(create_success("User has checked out", response))
            response = {"Status": "Error"}
            return JsonResponse(create_failure("Internal Error", response))
        except Exception as e:
            self.logger.error(e, exc_info=True)
            return JsonResponse(create_failure("Internal Error", "Fail"), status=500)

    def post(self, request: Request) -> JsonResponse:
        userid = request.query_params["UserID"]
        user = UserDetailsModel.objects.get(userid=userid)
        for index in range(10,20):
            temp = UserAttendanceLogsModel(
                userid=user.userid,
                checkin=(timezone.now() - timedelta(days=index)),
                checkout=(timezone.now() - timedelta(days=index)),
                createdon=(timezone.now() - timedelta(days=index)),
            )
            temp.save()
        return JsonResponse(create_success("Good to go"))


class AttendanceRegister(APIView):
    schema = AttendanceRegisterSchema()

    def __init__(self):
        self.logger = LoggerSetup(loggerName=str(__file__)).getLogger()

    def post(self, request: Request) -> JsonResponse:
        """
        Register attendance
        #### AttendanceRegister API

        #### Request Method
            POST

        #### Response parameter
        | Field name | Meaning | Types of |
        |:------:|:------:|:------:|
        | Message | message | String |
        | ReplyCode | code | String |
        | Data | List Of Datapoints | JSON |

        #### Response format
            JSON

        #### Response example
            {"Message": "Success", "ReplyCode": "Success" , "Data": {}}
        """
        try:
            userid = request.query_params["UserID"]
        except Exception as e:
            self.logger.error("Error in Attendance API - Request Payload : " + str(e))
            return JsonResponse(
                create_failure("Error in Request Payload", "Fail"), status=400
            )
        try:
            try:
                user = UserDetailsModel.objects.get(userid=userid)
            except Exception as e:
                self.logger.error("Error while fetching user")
                return JsonResponse(
                    create_failure("Error while fetching user", "Fail"), status=400
                )
            try:
                user_attendance_data = UserAttendanceLogsModel.objects.get(
                    userid=userid, createdon=timezone.now().date()
                )
            except Exception as e:
                user_attendance_data = UserAttendanceLogsModel(
                    userid=user.userid, createdon=timezone.now(), checkin=timezone.now()
                ).save()
                response = {"Status": "UserCheckedIn"}
                return JsonResponse(create_success("Success", response))
            if user_attendance_data.checkout is None:
                response = {"Status": "AlreadyCheckedIn"}
                return JsonResponse(
                    create_failure("User has already checked in", response),
                    status=404,
                )
            else:
                response = {"Status": "AlreadyCheckedOut"}
                return JsonResponse(
                    create_failure("User has already checked out", response),
                    status=404,
                )
        except Exception as e:
            self.logger.error(e, exc_info=True)
            return JsonResponse(create_failure("Internal Error", "Fail"), status=500)


class AttendanceClosure(APIView):
    schema = AttendanceClosureSchema()

    def __init__(self):
        self.logger = LoggerSetup(loggerName=str(__file__)).getLogger()

    def post(self, request: Request) -> JsonResponse:
        """
        Close the attendance
        #### AttendanceClosure API

        #### Request Method
            POST

        #### Response parameter
        | Field name | Meaning | Types of |
        |:------:|:------:|:------:|
        | Message | message | String |
        | ReplyCode | code | String |
        | Data | List Of Datapoints | JSON |

        #### Response format
            JSON

        #### Response example
            {"Message": "Success", "ReplyCode": "Success" , "Data": {}}
        """
        try:
            userid = request.query_params["UserID"]
        except Exception as e:
            self.logger.error("Error in Attendance API - Request Payload : " + str(e))
            return JsonResponse(
                create_failure("Error in Request Payload", "Fail"), status=400
            )
        try:
            try:
                UserDetailsModel.objects.get(userid=userid)
            except Exception as e:
                self.logger.error("Error while fetching user")
                return JsonResponse(
                    create_failure("Error while fetching user", "Fail"), status=400
                )
            try:
                user_attendance_data = UserAttendanceLogsModel.objects.get(
                    userid=userid, createdon=timezone.now().date()
                )
            except Exception as e:
                response = {"Status": "NotCheckedIn"}
                return JsonResponse(
                    create_failure("User has not checked in", response),
                    status=404,
                )
            if user_attendance_data.checkout is None:
                user_attendance_data.checkout = timezone.now()
                user_attendance_data.save()
                response = {"Status": "UserCheckedOut"}
                return JsonResponse(create_success("Success", response))
            else:
                response = {"Status": "AlreadyCheckedOut"}
                return JsonResponse(
                    create_failure("User has already checked out", response),
                    status=404,
                )
            response = {"Status": "Error"}
            return JsonResponse(create_failure("Internal Error", response))
        except Exception as e:
            self.logger.error(e, exc_info=True)
            return JsonResponse(create_failure("Internal Error", "Fail"), status=500)


class AttendancePaginatedLogs(APIView):
    schema = AttendancePaginatedLogsSchema()

    def __init__(self):
        self.logger = LoggerSetup(loggerName=str(__file__)).getLogger()
        self.StoredProcedureObject = StoredProcedure()
        self.Queries = Queries()

    def get(self, request: Request) -> JsonResponse:
        """
        Fetch Attendance Logs
        #### AttendancePaginatedLogs API

        #### Request Method
            GET

        #### Response parameter
        | Field name | Meaning | Types of |
        |:------:|:------:|:------:|
        | Message | message | String |
        | ReplyCode | code | String |
        | Data | List Of Datapoints | JSON |

        #### Response format
            JSON

        #### Response example
            {"Message": "Success", "ReplyCode": "Success" , "Data": {}}
        """
        try:

            try:
                userid = request.query_params["UserID"]
                # pagenumber = request.query_params["PageNumber"]
                # size = request.query_params.get("Size") or 10
            except Exception as e:
                self.logger.error(
                    "Error in Attendance API - Request Payload : " + str(e)
                )
                return JsonResponse(
                    create_failure("Error in Request Payload", "Fail"), status=400
                )

            try:
                user = UserDetailsModel.objects.get(userid=userid)
            except Exception as e:
                self.logger.error("Error while fetching user")
                return JsonResponse(
                    create_failure("Error while fetching user", "Fail"), status=400
                )
            ##########################################################################
            attendance_data = self.Queries.fetch_all_attendance_records_by_user(userid)
            ##########################################################################
            # try:
            #     attendance_data = {
            #         "TotalNumberOfPages": ceil(
            #             self.Queries.fetch_total_number_of_records(userid) / size
            #         ),
            #         "AttendanceData": self.StoredProcedureObject.fetch_attendance_pagination(
            #             userid=userid, pagenumber=pagenumber, size=size
            #         ),
            #     }
            #     self.logger.debug(attendance_data)
            # except Exception as e:
            #     self.logger.error("No logs found!, Error:", exc_info=True)
            #     return JsonResponse(
            #         create_failure("No logs found!", "Fail"), status=400
            #     )
            return JsonResponse(create_success("Success", data=attendance_data))
        except Exception as e:
            self.logger.error(e, exc_info=True)
            return JsonResponse(create_failure("Internal Error", "Fail"), status=500)


class AttendanceOverallReport(APIView):
    schema = AttendanceOverallReportSchema()

    def __init__(self):
        self.logger = LoggerSetup(loggerName=str(__file__)).getLogger()

    def get_monthly_attendance(self):
        print()

    def get(self, request: Request) -> JsonResponse:
        """
        Attendance Overall Report
        #### AttendanceOverallReport API

        #### Request Method
            GET

        #### Response parameter
        | Field name | Meaning | Types of |
        |:------:|:------:|:------:|
        | Message | message | String |
        | ReplyCode | code | String |
        | Data | List Of Datapoints | JSON |

        #### Response format
            JSON

        #### Response example
            {"Message": "Success", "ReplyCode": "Success" , "Data": {"TotalPresent": 1,"TotalAbsent": 3,"CurrentMonthAttendance": 1,"CurrentMonthAbsent": 3}}
        """
        try:
            try:
                userid = request.query_params["UserID"]
            except Exception as e:
                self.logger.error(
                    "Error in Attendance API - Request Payload : " + str(e)
                )
                return JsonResponse(
                    create_failure("Error in Request Payload", "Fail"), status=400
                )

            try:
                user = UserDetailsModel.objects.get(userid=userid)
            except Exception as e:
                self.logger.error("Error while fetching user")
                return JsonResponse(
                    create_failure("Error while fetching user", "Fail"), status=400
                )
            start_of_month = date(date.today().year, date.today().month, 1)
            current_date = timezone.now().date()
            date_of_joining = user.dateofjoining.date()
            if date_of_joining > start_of_month:
                delta_current_month = current_date - date_of_joining
            else:
                delta_current_month = current_date - start_of_month
            delta_total_attendance_days = current_date - date_of_joining

            total_attendance_days = delta_total_attendance_days.days
            current_month_attendance_days = delta_current_month.days

            try:
                total_attendance = UserAttendanceLogsModel.objects.filter(
                    userid=userid
                ).count()
                current_month_attendance = UserAttendanceLogsModel.objects.filter(
                    userid=userid, createdon__gte=start_of_month
                ).count()
                user_attendance_data = {
                    "TotalPresent": total_attendance,
                    "TotalAbsent": total_attendance_days - total_attendance,
                    "CurrentMonthAttendance": current_month_attendance,
                    "CurrentMonthAbsent": current_month_attendance_days
                    - current_month_attendance,
                }
            except Exception as e:
                self.logger.error("Error while fetching logs!", exc_info=True)
                return JsonResponse(
                    create_failure("Error while fetching logs!", "Fail"),
                    status=400,
                )
            print(user_attendance_data)
            return JsonResponse(create_success("Success", data=user_attendance_data))
        except Exception as e:
            self.logger.error(e, exc_info=True)
            return JsonResponse(create_failure("Internal Error", "Fail"), status=500)


class AttendanceApprovalStatus(APIView):
    schema = AttendanceMentorInputSchema()

    def __init__(self):
        self.logger = LoggerSetup(loggerName=str(__file__)).getLogger()
        self.StoredProcedureObject = StoredProcedure()

    def get(self, request: Request) -> JsonResponse:
        """
        Attendance Mentor Approval Status
        #### AttendanceApprovalStatus API

        #### Request Method
            GET

        #### Response parameter
        | Field name | Meaning | Types of |
        |:------:|:------:|:------:|
        | Message | message | String |
        | ReplyCode | code | String |
        | Data | List Of Datapoints | JSON |

        #### Response format
            JSON

        #### Response example
            {"Message": "Success", "ReplyCode": "Success" , "Data": {}}
        """
        try:
            try:
                mentor = request.query_params["Mentor"]
            except Exception as e:
                self.logger.error("Error in Request Payload! Error:" + str(e))
                return JsonResponse(
                    create_failure("Error in Request Payload", "Fail"), status=400
                )
            data = self.StoredProcedureObject.fetch_approval_status_by_mentor(mentor)
            return JsonResponse(create_success("Success", data=data))
        except Exception as e:
            self.logger.error(e, exc_info=True)
            return JsonResponse(create_failure("Internal Error", "Fail"), status=500)


class AttendanceMentorApproval(APIView):

    schema = AttendanceMentorApprovalSchema()

    def __init__(self):
        self.logger = LoggerSetup(loggerName=str(__file__)).getLogger()

    def post(self, request: Request) -> JsonResponse:
        """
        Attendance Mentor Approval
        #### AttendanceMentorApproval API

        #### Request Method
            POST

        #### Response parameter
        | Field name | Meaning | Types of |
        |:------:|:------:|:------:|
        | Message | message | String |
        | ReplyCode | code | String |
        | Data | List Of Datapoints | JSON |

        #### Response format
            JSON

        #### Response example
            {"Message": "Success", "ReplyCode": "Success" , "Data": {}}
        """
        try:
            try:
                mentor = request.query_params.get("Mentor")
                userid = request.query_params["UserID"]
                approvalstatus = request.query_params["ApprovalStatus"]
                createdon = request.query_params["CreatedOn"]

                if approvalstatus not in ["Approved", "Pending", "Disapproved"]:
                    raise ValueError("Approval")

            except Exception as e:
                self.logger.error("Error in Request Payload! Error:" + str(e))
                return JsonResponse(
                    create_failure("Error in Request Payload", "Fail"), status=400
                )
            try:
                user = UserDetailsModel.objects.get(userid=userid, mentor=mentor)
            except Exception as e:
                self.logger.error(f"Error while fetching user:{e}")
                return JsonResponse(
                    create_failure("Error while fetching user", "Fail"), status=400
                )
            try:
                user_attendance_data = UserAttendanceLogsModel.objects.get(
                    userid=userid,
                    createdon=datetime.strptime(createdon, "%Y-%m-%d"),
                    approvalstatus="Pending",
                )
            except Exception as e:
                self.logger.error(
                    "Cannot find logs with mentioned details", exc_info=True
                )
                return JsonResponse(
                    create_failure("Cannot find logs with mentioned details", "Fail"),
                    status=400,
                )
            user_attendance_data.approvalstatus = approvalstatus
            user_attendance_data.approvalstatusdate = timezone.now()
            user_attendance_data.save()
            response = {"Status": f"UserStatusSetTo{approvalstatus}"}
            return JsonResponse(create_success("Success", response))
        except Exception as e:
            self.logger.error(e, exc_info=True)
            return JsonResponse(create_failure("Internal Error", "Fail"), status=500)
