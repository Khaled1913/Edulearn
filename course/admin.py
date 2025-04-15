from django.contrib import admin
from .models import Course,Lesson,Student
# Register your models here.
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Student)