import json

from django.shortcuts import renderu
from rest_framework.views import APIView
from rest_framework.request import Request
from django.http.response import JsonResponse
import requests

from common.create_response import create_failure, create_success
from user_management.serializers import UserDetailsSerializer
from user_management.models import UserDetails as UserDetailsModel
from common.read_logger import LoggerSetup
from common.swagger_schema import (
    BasicAuthenticationLoginSchema,
    SSOAuthenticationLoginSchema,
)
from common.authentication import encode_auth_token


class UserAuthenticationLogin(APIView):
    schema = BasicAuthenticationLoginSchema()

    def __init__(self):
        self.logger = LoggerSetup(loggerName=str(__file__)).getLogger()

    def post(self, request: Request) -> JsonResponse:
        """
        User Authentication
        #### UserAuthenticationLogin API

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
            self.email = request.data["Email"]
            self.password = request.data["Password"]
        except Exception as e:
            self.logger.error("Error in Login API - Request Payload : " + str(e))
            return JsonResponse(
                create_failure("Error in Request Payload", "Fail"), status=400
            )

        try:
            try:
                user = UserDetailsModel.objects.get(emailaddress=self.email)
            except Exception as e:
                try:
                    self.logger.info("Redirecting to Organization Email Address")
                    user = UserDetailsModel.objects.get(
                        organizationemailaddress=self.email
                    )
                except Exception as e:
                    self.logger.error("Error in Login API - Wrong Email : " + str(e))
                    return JsonResponse(
                        create_failure("Invalid Email", "Fail"), status=403
                    )
            if user.userstatus == "Disable":
                self.logger.error("Error in Login API - Disabled User")
                return JsonResponse(create_failure("User Disabled", "Fail"), status=403)
            if self.password == user.password:
                jwt_response = encode_auth_token({"userid": user.userid})
                if jwt_response.get("status") in ["ERROR", None]:
                    raise Exception("Could not encode JWT")
                response = {
                    "JWT": jwt_response.get("message"),
                    "UserID": user.userid,
                    "FirstName": user.firstname,
                    "LastName": user.lastname,
                    "EmailAddress": user.emailaddress,
                    "OrganizantionEmailAddress": user.organizationemailaddress,
                    "Role": user.role,
                    "Mentor": user.mentor,
                }
            else:
                self.logger.error("Error in Login API - Wrong Password")
                return JsonResponse(
                    create_failure("Invalid Password", "Fail"), status=403
                )
            return JsonResponse(create_success("Authorization Successful!", response))
        except Exception as e:
            self.logger.error("Error in Login API : " + str(e))
            return JsonResponse(
                create_failure("Error in Login API", "Fail"), status=500
            )


class UserAuthenticationLogout(APIView):
    def __init__(self):
        self.logger = LoggerSetup(loggerName=str(__file__)).getLogger()

    def post(
        self,
    ):
        print("Logging out")


class UserSSOAuthenticationLogin(APIView):
    """
    User Azure SSO Authentication
    #### UserSSOAuthenticationLogin API

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

    schema = SSOAuthenticationLoginSchema()

    def __init__(self):
        self.logger = LoggerSetup(loggerName=str(__file__)).getLogger()
        self.mentor_flag=0

    def post(self, request: Request) -> JsonResponse:
        try:
            azure_access_token = request.META["HTTP_LOGINTOKEN"]
        except Exception as e:
            self.logger.error("Error while fetching Login Token")
            return JsonResponse(
                create_failure("Error in fetching Login Token", "Fail"), status=400
            )
        try:
            user_data = requests.get(
                "https://graph.microsoft.com/v1.0/me",
                headers={"Authorization": f"Bearer {azure_access_token}"},
            ).json()

            # if user_data.get("error").get("code")=="InvalidAuthenticationToken":
            #     raise Exception("Issue with Authentication Token")
            self.email = user_data["mail"]
            try:
                users = UserDetailsModel.objects.get(emailaddress=self.email)
            except Exception as e:
                try:
                    user = UserDetailsModel.objects.get(
                        organizationemailaddress=self.email
                    )
                except Exception as e:
                        user = UserDetailsModel.objects.filter(mentor=self.email)
                        self.mentor_flag = 1
                        self.full_name = user_data.get("displayName")
                        if self.full_name is not None:
                            try:
                                self.first_name = self.full_name.split(" ")[0]
                            except:
                                self.first_name = None
                            try:
                                self.last_name = self.full_name.split(" ")[1]
                            except:
                                self.last_name = None
            except Exception as e:
                self.logger.error("User Not Found : ", exc_info=True)
                return JsonResponse(create_failure("User Not Found", "Fail"), status=403)
            #put functionality for Enable and Disable
            if self.mentor_flag != 1 and user.userstatus=="Disable":
                self.logger.error("Error in Login API - Disabled User")
                return JsonResponse(create_failure("User Disabled", "Fail"), status=403)
            
            # jwt_response = encode_auth_token({"userid": user.userid})
            # if jwt_response.get("status") in ["ERROR", None]:
            #     raise Exception("Could not encode JWT")
            if self.mentor_flag:
                response = {
                    # "JWT": str(jwt_response.get("message")),
                    "FirstName": self.first_name,
                    "LastName": self.last_name,
                    "EmailAddress": self.email,
                    "OrganizantionEmailAddress": self.email,
                    "Role": "Mentor",
                    "Mentor": None,
                }
            else:
                response = {
                    # "JWT": str(jwt_response.get("message")),
                    "UserID": user.userid,
                    "FirstName": user.firstname,
                    "LastName": user.lastname,
                    "EmailAddress": user.emailaddress,
                    "OrganizantionEmailAddress": user.organizationemailaddress,
                    "Role": user.role,
                    "Mentor": user.mentor,
                }
            return JsonResponse(create_success("Authorization Successful!", response))

        except Exception as e:
            self.logger.error(e, exc_info=True)
            return JsonResponse(create_failure("Internal Error", "Fail"), status=500)
