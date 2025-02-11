from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views
from api.views import RegisterView, TrainCreateView, seat_availability, book_seat, booking_details

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', RegisterView.as_view()),
    path('login/', views.obtain_auth_token),
    path('trains/', TrainCreateView.as_view()),
    path('availability/', seat_availability),
    path('book/<int:train_id>/', book_seat),
    path('booking/<int:booking_id>/', booking_details),
]