from django.urls import path
from orders import views

urlpatterns = [
    path("create/", views.CreateOrderView.as_view(), name="create_order"),
    path(
        "history/<str:pk>",
        views.CustomerShipmentHistoryView.as_view(),
        name="show_history",
    ),
]
