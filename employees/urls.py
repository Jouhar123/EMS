from .views import (
    EmployeeListCreateView,
    EmployeeDetailView,
    EmployeeUpdateView,
    AttendanceListView,
    UserListView, 
    UserDeleteView,
    AttendanceCreateView,
    AttendanceUpdateView,
    AttendanceDeleteView,
    AttendanceByEmployeeView,

)

from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import SignupView

urlpatterns = [
   path('employees/', EmployeeListCreateView.as_view(), name='employee-list-create'),
   path('employees/<int:pk>/', EmployeeDetailView.as_view(), name='employee-detail'),

    path("attendance/", AttendanceCreateView.as_view()),
    path("attendance/<uuid:attendance_id>/", AttendanceUpdateView.as_view()),
    path("attendance/<uuid:attendance_id>/delete/", AttendanceDeleteView.as_view()),
    path("attendance/employee/<int:employee_id>/", AttendanceByEmployeeView.as_view()),

    path("signup/", SignupView.as_view()),
    path("login/", TokenObtainPairView.as_view()),
    path("users/", UserListView.as_view()),
    path("users/<int:pk>/", UserDeleteView.as_view()),


]
