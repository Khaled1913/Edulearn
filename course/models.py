from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.IntegerField(help_text="Duration in hours")
    thumbnail = models.ImageField(upload_to='course_thumbnails/', null=True, blank=True)
    created_at = models.DateTimeField( default=timezone.now)

    def __str__(self):
        return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content = models.TextField()
    video_url = models.URLField(null=True, blank=True)
    completion_status = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    enrolled_courses = models.ManyToManyField(Course, related_name='students', blank=True)
    completed_lessons = models.ManyToManyField(Lesson, related_name='completed_by', blank=True)
    progress = models.FloatField(default=0)  # Optional field to store progress
    
    def update_progress(self, course):
        """
        Calculate and update progress for a specific course.
        """
        total_lessons = course.lessons.count()
        # Only count completed lessons that belong to this course.
        completed_lessons = self.completed_lessons.filter(course=course).count()
        self.progress = (completed_lessons / total_lessons) * 100 if total_lessons > 0 else 0
        self.save()
    
    def __str__(self):
        return self.name
