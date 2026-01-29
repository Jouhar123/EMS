import uuid
from django.db import models
from django.contrib.auth.models import User

import uuid
from django.db import models

class Employee(models.Model):
    employee_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.employee_id})"



# employees/models.py
import uuid
from django.db import models
from django.contrib.auth.models import User

class Attendance(models.Model):
    PRESENT = "Present"
    ABSENT = "Absent"

    STATUS_CHOICES = [
        (PRESENT, "Present"),
        (ABSENT, "Absent"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="attendance"
    )
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ("employee", "date")
        ordering = ["-date"]

    def __str__(self):
        return f"{self.employee.username} - {self.date}"
