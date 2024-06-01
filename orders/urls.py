from django.urls import path
from orders import views

urlpatterns = [
    path("create/", views.CreateOrderView.as_view(), name="create_order"),
    path(
        "history/",
        views.CustomerShipmentHistoryView.as_view(),
        name="customer_history",
    ),
]
