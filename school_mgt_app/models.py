from django.db import models
from django.contrib.auth.models import AbstractUser

# 1. Custom User Model
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('director', 'Director'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email


# 2. Form/Class structure (Moved up so others can reference it)
class Form(models.Model):
    name = models.CharField(max_length=20) # e.g., "Form 1A"

    def __str__(self):
        return self.name


# 3. Teacher Model (Linked to User)
class Teacher(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('on leave', 'On Leave'),
    ]
    
    # Links to the custom User model above
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    assigned_forms = models.ManyToManyField(Form, blank=True)

    def get_initials(self):
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name[0]}{self.user.last_name[0]}".upper()
        return "T"

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.subject}"


# 4. Student Model
class Student(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=20, unique=True)
    # Using ForeignKey to Form is better than CharField for data integrity
    class_name = models.CharField(max_length=50) 
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    parent_name = models.CharField(max_length=150)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# 5. Class model (Reference to Teacher)
class Class(models.Model):
    name = models.CharField(max_length=50)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


# 6. Fees Model
class Fee(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=10,
        choices=(('pending','pending'),('paid','paid')),
        default='pending'
    )

    def __str__(self):
        return f"{self.student} - {self.amount} - {self.status}"