from django.urls import path
from . import views

urlpatterns = [
    path("api/UserDetails", views.UserDetails.as_view()),
    path("api/InternsUnderMentor", views.InternsUnderMentor.as_view()),
    path("api/FetchAllUsersByHR", views.FetchAllUsersByHR.as_view()),
    path("api/FilterADUsers", views.FetchAzureADUsers.as_view()),
]