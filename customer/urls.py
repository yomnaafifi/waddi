from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.CustomerSignupView.as_view(), name="customer_signup"),
    path(
        "details/<int:id>", views.CustomerDetailsView.as_view(), name="customer_details"
    ),
    path("all/", views.ListAllCustomersView.as_view()),
]
