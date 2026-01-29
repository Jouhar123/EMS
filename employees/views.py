from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from .models import Employee, Attendance
from .serializers import EmployeeSerializer, AttendanceSerializer ,SignupSerializer, UserSerializer
from rest_framework.viewsets import ModelViewSet
from .permissions import IsAdminOrReadOnly
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from datetime import datetime
from django.shortcuts import get_object_or_404



class EmployeeListCreateView(generics.ListCreateAPIView):
    queryset = Employee.objects.all().order_by('-created_at')
    serializer_class = EmployeeSerializer

class EmployeeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class EmployeeUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
  

#  viewset auth
class EmployeeViewSet(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAdminOrReadOnly]

class AttendanceViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]


class AttendanceByEmployeeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, employee_id):
        month = request.GET.get("month")  

        qs = Attendance.objects.filter(employee_id=employee_id)

        if month:
            year, month = map(int, month.split("-"))
            qs = qs.filter(date__year=year, date__month=month)

        serializer = AttendanceSerializer(qs, many=True)
        return Response(serializer.data)



class AttendanceListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_staff:  # admin
            attendance = Attendance.objects.all()
        else:
            attendance = Attendance.objects.filter(employee__user=request.user)

        serializer = AttendanceSerializer(attendance, many=True)
        return Response(serializer.data)




class AttendanceCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        serializer = AttendanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class AttendanceDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, request, attendance_id):
        attendance = get_object_or_404(Attendance, id=attendance_id)
        attendance.delete()
        return Response({"message": "Attendance deleted"})



class AttendanceUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser] # Only Admin can reach here

    def put(self, request, attendance_id):
        return self.update(request, attendance_id, partial=False)

    def patch(self, request, attendance_id):
        return self.update(request, attendance_id, partial=True)

    def update(self, request, attendance_id, partial):
        attendance = get_object_or_404(Attendance, id=attendance_id)
        serializer = AttendanceSerializer(
            attendance, data=request.data, partial=partial
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Signup 
class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created"}, status=201)
        return Response(serializer.errors, status=400)

# Login
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user = authenticate(
            username=request.data.get("username"),
            password=request.data.get("password")
        )

        if not user:
            return Response({"error": "Invalid credentials"}, status=401)

        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "is_admin": user.is_staff,
            "username": user.username,
        })

# Users
class UserListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class UserDeleteView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            user.delete()
            return Response({"message": "User deleted"})
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
