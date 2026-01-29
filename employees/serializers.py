from rest_framework import serializers
from .models import Employee, Attendance
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models import Attendance

User = get_user_model()

# Employee
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"

# Attendence
# class AttendanceSerializer(serializers.ModelSerializer):
#     employee_name = serializers.CharField(
#         source="employee.username", read_only=True
#     )

#     class Meta:
#         model = Attendance
#         fields = [
#             "id",
#             "employee",
#             "employee_name",
#             "date",
#             "status",
#         ]


# Signup
class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'email': {'required': True, 'allow_blank': False}}

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_staff=False
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff']




class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'
        validators = [] 
    def validate(self, attrs):
        if not self.instance: 
            employee = attrs.get('employee')
            date = attrs.get('date')
            if Attendance.objects.filter(employee=employee, date=date).exists():
                raise serializers.ValidationError("Attendance for this date already exists.")
        return attrs
