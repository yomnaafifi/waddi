from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.CustomerSignupView.as_view(), name="customer_signup"),
    path("<int:id>/", views.CustomerDetailsView.as_view(), name="customer_details"),
    path("/", views.CustomersView.as_view()),
]
