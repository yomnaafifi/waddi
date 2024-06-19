from django.urls import path
from orders import views

urlpatterns = [
    path("pricing/", views.CalculatePriceView.as_view(), name="calculate_price"),
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
    path(
        "<str:id>/state/<str:state>",
        views.ChangeOrderState.as_view(),
        name="change_state",
    ),
    # path("predict/", views.predict),
    path("test/", views.testingshortserializer.as_view()),
    # path("testnew/", views.TESTNEWSER.as_view()),
]
