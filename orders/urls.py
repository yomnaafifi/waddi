from django.urls import path
from customer import views

urlpatterns = [
    path("create/", views.CreateOrderView.as_view(), name="create_order"),
]
