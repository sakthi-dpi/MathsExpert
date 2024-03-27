# admin.py
from django.contrib import admin
from .models import Student, Teacher, Course, QuestionPaper, ExamSchedule, ClassTimetable

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Course)
admin.site.register(QuestionPaper)
admin.site.register(ExamSchedule)
admin.site.register(ClassTimetable)

