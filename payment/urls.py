from django.urls import path
from . import views

urlpatterns = [
    path("createtx/", views.createtx.as_view(), name="create_tx"),
    path("drivertxhistory/", views.drivertxhistory.as_view(), name="driver_tx_history"),
]
