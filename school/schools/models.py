import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Schools(models.Model):
    title = models.CharField(max_length=20, blank=False, null=False)
    number_of_student = models.IntegerField(blank=False, null=False, validators=[MinValueValidator(0), MaxValueValidator(50)])

    @property
    def details_context(self):
        return{
            "id": self.pk,
            "title": self.title,
            "number_of_student": self.number_of_student,
        }

class Student(models.Model):
    schools = models.ForeignKey(Schools, blank=False, null=False, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20, blank=False, null=False)
    last_name = models.CharField(max_length=20, blank=False, null=False)
    student_id = models.UUIDField(null=False, blank=False, default=uuid.uuid4, editable=True)
    
    @property
    def details_context(self):
        return{
            "id": self.pk,
            "schools": self.schools.details_context,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "student_id": self.student_id
        }