import coreapi
from common.create_response import create_failure, create_success
from common.read_logger import LoggerSetup
from common.swagger_schema import (
    UserManagementInternsUnderMentorSchema,
    UserManagementSchema,
)
from django.core.mail import send_mail
from django.core.serializers import serialize
from django.http.response import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer

from .models import UserDetails as UserDetailsModel
from .serializers import UserDetailsSerializer
from .sqlqueries import StoredProcedure, Queries
from common.authentication import encode_auth_token, decode_auth_token
from common.common_api import AzureAD


# Create your views here.
class UserDetails(APIView):

    schema = UserManagementSchema()

    def __init__(self):
        self.logger = LoggerSetup(loggerName=str(__file__)).getLogger()

    def get(self, request: Request) -> JsonResponse:
        """
        Get User Details
        #### UserDetails API

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
                self.userid = request.query_params["UserID"]
            except Exception as e:
                self.logger.error("Error while fetching query parameter")
                return JsonResponse(
                    create_failure(
                        "Error while fetching query parameter(UserID)", "Fail"
                    ),
                    status=400,
                )
            try:
                user_info = UserDetailsModel.objects.filter(userid=self.userid)
            except Exception as e:
                self.logger.error("Error while fetching user")
                return JsonResponse(
                    create_failure("Error while fetching user", "Fail"), status=400
                )
            user_data = UserDetailsSerializer(user_info, many=True)
            if len(user_data.data) == 0:
                return JsonResponse({})
            filter_key = {
                "userid": "UserID",
                "userstatus": "UserStatus",
                "role": "Role",
                "dateofjoining": "DateOfJoining",
                "mentor": "Mentor",
                "currentproject": "CurrentProject",
                "projectmentor": "ProjectMentor",
                "password": "Password",
                "firstname": "FirstName",
                "middlename": "MiddleName",
                "lastname": "LastName",
                "contactno": "ContactNo",
                "emailaddress": "EmailAddress",
                "organizationemailaddress": "OrganizationEmailAddress",
                "createddate": "CreatedDate",
            }
            filtered_data = dict(
                (filter_key[key], value) for key, value in user_data.data[0].items()
            )
            return JsonResponse(create_success("Success", filtered_data))
        except Exception as e:
            self.logger.error(e, exc_info=True)
            return JsonResponse(create_failure("Internal Error", "Fail"), status=500)

    def post(self, request: Request) -> JsonResponse:
        # temp = UserDetailsModel(
        #     userid="CL1002",
        #     role="test",
        #     password="admin",
        #     firstname="test",
        #     lastname="test",
        #     middlename="test",
        #     contactno="test",
        #     emailaddress="test9012@test.com",
        #     organizationemailaddress="manas@celebaltech.com",
        # )
        # temp.save()
        # return JsonResponse(create_success("Good to go"))
        """
        Register User
        #### UserDetails API

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
                self.role = request.data["Role"]
                self.password = request.data["Password"]
                self.firstname = request.data["FirstName"]
                self.lastname = request.data["LastName"]
                self.middlename = request.data.get("MiddleName")
                self.contactno = request.data["ContactNo"]
                self.emailaddress = request.data["EmailAddress"]
                self.organizationemailaddress = request.data.get(
                    "OrganizationEmailAddress"
                )
                self.dateofjoining = request.data.get("DateOfJoining")
                self.mentor = request.data.get("Mentor")
                self.currentproject = request.data.get("CurrentProject")
                self.projectmentor = request.data.get("ProjectMentor")
            except Exception as e:
                self.logger.error("Error in Request Payload")
                return JsonResponse(
                    create_failure("Error in Request Payload", "Fail"), status=400
                )

            user = UserDetailsModel(
                role=self.role,
                password=self.password,
                firstname=self.firstname,
                lastname=self.lastname,
                middlename=self.middlename,
                contactno=self.contactno,
                emailaddress=self.emailaddress,
                organizationemailaddress=self.organizationemailaddress,
                dateofjoining=self.dateofjoining,
                mentor=self.mentor,
                currentproject=self.currentproject,
                projectmentor=self.projectmentor,
            )
            user.save()
            return JsonResponse(
                create_success("User Registration Successful!", {"Status": "Success"})
            )
        except Exception as e:
            self.logger.error("Error in Register API")
            return JsonResponse(
                create_failure(f"Error in Register API:{e}", "Fail"), status=500
            )

    def put(self, request: Request) -> JsonResponse:
        """
        Update User
        #### UserDetails API

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
                self.userid = request.data.get("UserID")
                self.role = request.data.get("Role")
                self.password = request.data.get("Password")
                self.firstname = request.data.get("FirstName")
                self.lastname = request.data.get("LastName")
                self.middlename = request.data.get("MiddleName")
                self.contactno = request.data.get("ContactNo")
                self.emailaddress = request.data.get("EmailAddress")
                self.organizationemailaddress = request.data.get(
                    "OrganizationEmailAddress"
                )
                self.userstatus = request.data.get("UserStatus")
                self.dateofjoining = request.data.get("DateOfJoining")
                self.mentor = request.data.get("Mentor")
                self.currentproject = request.data.get("CurrentProject")
                self.projectmentor = request.data.get("ProjectMentor")
                if self.userid is None:
                    raise Exception("Missing UserID")
            except Exception as e:
                self.logger.error("Error in Request Payload", exc_info=True)
                return JsonResponse(
                    create_failure("Error in Request Payload", "Fail"), status=400
                )
            try:
                user = UserDetailsModel.objects.get(userid=self.userid)
            except Exception as e:
                self.logger.error("Error while fetching user", exc_info=True)
                return JsonResponse(
                    create_failure("Error while fetching user", "Fail"), status=400
                )

            user.role = self.role or user.role
            user.password = self.password or user.password
            user.firstname = self.firstname or user.firstname
            user.lastname = self.lastname or user.lastname
            user.middlename = self.middlename or user.middlename
            user.contactno = self.contactno or user.contactno
            user.emailaddress = self.emailaddress or user.emailaddress
            user.organizationemailaddress = (
                self.organizationemailaddress or user.organizationemailaddress
            )
            user.userstatus = self.userstatus or user.userstatus
            user.dateofjoining = self.dateofjoining or user.dateofjoining
            user.mentor = self.mentor or user.mentor
            user.currentproject = self.currentproject or user.currentproject
            user.projectmentor = self.projectmentor or user.projectmentor
            user.save()
            return JsonResponse(
                create_success("User Updation Successful!", {"Status": "Success"})
            )
        except Exception as e:
            self.logger.error("Error in Register API")
            return JsonResponse(
                create_failure(f"Error in Register API:{e}", "Fail"), status=500
            )

    def delete(self, request: Request) -> JsonResponse:
        """
        Delete User
        #### UserDetails API

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
                self.userid = request.query_params.get("UserID")
            except Exception as e:
                self.logger.error("Error in Request Payload")
                return JsonResponse(
                    create_failure("Error in Request Payload", "Fail"), status=400
                )
            print(self.userid)
            try:
                user = UserDetailsModel.objects.get(userid=self.userid)
            except Exception as e:
                self.logger.error("Error while fetching user")
                return JsonResponse(
                    create_failure("Error while fetching user", "Fail"), status=400
                )
            user.delete()
            return JsonResponse(
                create_success("User Deletion Successful!", {"Status": "Success"})
            )
        except Exception as e:
            self.logger.error("Error in Register API")
            return JsonResponse(
                create_failure(f"Error in Register API:{e}", "Fail"), status=500
            )


class InternsUnderMentor(APIView):
    schema = UserManagementInternsUnderMentorSchema()

    def __init__(self):
        self.logger = LoggerSetup(loggerName=str(__file__)).getLogger()
        self.StoredProcedureObject = StoredProcedure()

    def get(self, request: Request) -> JsonResponse:
        """
        Get Interns Under Mentor
        #### InternsUnderMentor API

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
                self.logger.error(
                    "Error in Attendance API - Request Payload : " + str(e)
                )
                return JsonResponse(
                    create_failure("Error in Request Payload", "Fail"), status=400
                )

            try:
                user = UserDetailsModel.objects.filter(mentor=mentor)
                if user.count() < 1:
                    raise Exception("Error while fetching user")
            except Exception as e:
                self.logger.error("Error while fetching user")
                return JsonResponse(
                    create_failure("Error while fetching user", "Fail"), status=400
                )

            try:
                interns_list = self.StoredProcedureObject.fetch_interns_under_mentor(
                    mentor=mentor
                )
                self.logger.debug(interns_list)
            except Exception as e:
                self.logger.error("No logs found!, Error:", exc_info=True)
                return JsonResponse(
                    create_failure("No logs found!", "Fail"), status=400
                )
            return JsonResponse(create_success("Success", data=interns_list))
        except Exception as e:
            self.logger.error(e, exc_info=True)
            return JsonResponse(create_failure("Internal Error", "Fail"), status=500)


class FetchAllUsersByHR(ListAPIView):
    schema = UserManagementInternsUnderMentorSchema()

    def __init__(self):
        self.logger = LoggerSetup(loggerName=str(__file__)).getLogger()
        self.StoredProcedureObject = StoredProcedure()
        self.QueryObject = Queries()

    def get(self, request: Request) -> JsonResponse:
        """
        Get List of All Users
        #### FetchAllUsersByHR API

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
            # try:
            #     pagenumber = request.query_params["PageNumber"]
            #     size = request.query_params.get("Size") or 10
            # except Exception as e:
            #     self.logger.error(
            #         "Error in Attendance API - Request Payload : " + str(e)
            #     )
            #     return JsonResponse(
            #         create_failure("Error in Request Payload", "Fail"), status=400
            #     )
            fetched_data = self.QueryObject.fetch_all_interns()
            # fetched_data = self.StoredProcedureObject.fetch_all_interns(
            #     size=size, pagenumber=pagenumber
            # )
            return JsonResponse(
                create_success("Success", data=fetched_data), status=200
            )
        except Exception as e:
            self.logger.error(e, exc_info=True)
            return JsonResponse(create_failure("Internal Error", "Fail"), status=500)


class ForgetPassword:
    def __init__(self):
        self.logger = LoggerSetup(loggerName=str(__file__)).getLogger()

    def send_activation_link(self):
        self.jwt_token = encode_auth_token(
            {"userid": self.user.userid}, timedeltavalue=15
        )
        message = render_to_string(
            "authentication/index.html",
            {
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": token.token,
            },
        )
        send_mail(
            "Forget Password Link",
            message,
            "bharat.jain@celebaltech.com",
            [self.user.emailaddress],
            fail_silently=False,
        )

    def post(self, request: Request) -> JsonResponse:
        try:
            try:
                self.input_email_address = request.data["EmailAddress"]
            except Exception as e:
                self.logger.error(
                    "Error in Attendance API - Request Payload : " + str(e)
                )
                return JsonResponse(
                    create_failure("Error in Request Payload", "Fail"), status=400
                )
            try:
                user_query_set_regular_email_address = UserDetailsModel.objects.filter(
                    emailaddress=self.input_email_address
                )
                if user_query_set.exists():
                    self.user = user_query_set_regular_email_address
                else:
                    user_query_set_organization_email_address = (
                        UserDetailsModel.objects.filter(
                            organizationemailaddress=self.input_email_address
                        )
                    )
                    if user_query_set.exists():
                        self.user = user_query_set_organization_email_address
                    else:
                        raise Exception("User Not Found")
            except Exception as e:
                self.logger.error("Error while fetching user")
                return JsonResponse(
                    create_failure("Error while fetching user", "Fail"), status=400
                )
            self.send_activation_link()
        except Exception as e:
            self.logger.error(e, exc_info=True)
            return JsonResponse(create_failure("Internal Error", "Fail"), status=500)

    def get(self, request: Request) -> JsonResponse:
        print("hello")


class FetchAzureADUsers(APIView):
    def __init__(self):
        self.logger = LoggerSetup(loggerName=str(__file__)).getLogger()

    def get(self, request: Request) -> JsonResponse:
        try:
            try:
                self.input_string = request.query_params["Input"]
            except Exception as e:
                self.logger.error(
                    "Error in Attendance API - Request Payload : " + str(e)
                )
                return JsonResponse(
                    create_failure("Error in Request Payload", "Fail"), status=400
                )
            ad_object = AzureAD()
            return JsonResponse(
                create_success(
                    "Success", data=ad_object.fetch_all_users(self.input_string) or []
                ),
                status=200,
            )
        except Exception as e:
            self.logger.error(e, exc_info=True)
            return JsonResponse(create_failure("Internal Error", "Fail"), status=500)