from django.urls import path
from . import views


urlpatterns = [
    path("api/AuthenticationLogin", views.UserAuthenticationLogin.as_view()),
    path("api/AuthenticationLogout", views.UserAuthenticationLogout.as_view()),
    path("api/AuthenticationSSO",views.UserSSOAuthenticationLogin.as_view())
]
