# models.py
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_company = models.BooleanField(default=False)
    username = models.CharField(max_length=150, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name='custom_user_set'
    )
    def __str__(self):
        return self.username


    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_permissions'
    )
    

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    academic_level = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    cv = models.FileField(upload_to='student_cvs', blank=True, null=True)
    transcript = models.FileField(upload_to='student_transcripts', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    contact_person = models.CharField(max_length=100, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Internship(models.Model):
    title = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='companies')
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    requirements = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Application(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='students')
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE, related_name='interships')
    status = models.CharField(max_length=50, default='Pending')
    application_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student.last_name + ' ' + self.internship.title