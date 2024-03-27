# models.py
from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    passport_photo = models.ImageField(upload_to='passport_photos/')
    date_of_birth = models.DateField()
    qualification = models.CharField(max_length=100)
    employment_status = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()
    guardian_contact_number = models.CharField(max_length=15)
    contact_address = models.TextField()
    date_of_joining = models.DateField()
    medium_of_study = models.CharField(max_length=50)
    batch_type = models.CharField(max_length=50)
    class_type = models.CharField(max_length=50)
    recommended_by = models.CharField(max_length=100)
    approved = models.BooleanField(default=False)

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Course(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

class ExamSchedule(models.Model):
    exam_date = models.DateField()
    exam_time = models.TimeField()

class ClassTimetable(models.Model):
    day_of_week = models.CharField(max_length=20)
    start_time = models.TimeField()
    end_time = models.TimeField()

class QuestionPaper(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

