from django.urls import path
from .views import ReservationCreateView, MyReservationsView

urlpatterns = [
    path("", ReservationCreateView.as_view(), name="reservation_create"),
    path("me", MyReservationsView.as_view(), name="my_reservations"),
]