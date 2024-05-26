from django.urls import path
from . import views


urlpatterns = [
    path("signup/", views.DriverSignupView.as_view(), name="driver_signup"),
    path("profile/", views.DriverDetailsView.as_view(), name="driver_details"),
]
