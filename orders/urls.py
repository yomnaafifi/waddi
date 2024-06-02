from django.urls import path
from orders import views

urlpatterns = [
    path("create/", views.CreateOrderView.as_view(), name="create_order"),
    path(
        "customer/history/",
        views.CustomerShipmentHistoryView.as_view(),
        name="customer_history",
    ),
    path(
        "driver/history/",
        views.DriverShipmentHistoryView.as_view(),
        name="driver_history",
    ),
    # path("testnew/", views.TESTNEWSER.as_view()),
]
