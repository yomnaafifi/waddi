from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.CustomerSignupView.as_view(), name = 'customer_signup' ),
]