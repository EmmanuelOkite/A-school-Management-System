from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm, StudentForm
from django.contrib.auth import authenticate, login, logout
from .models import User, Student, Teacher, Class, Fee
from django.contrib.auth.decorators import login_required
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
# Create your views here.

# Registration view
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)   # 🔥 don't save yet

            # ✅ get role from form
            user.role = request.POST.get('role')

            user.save()  # ✅ now save with role

            messages.success(request, "Account created successfully!")
            return redirect('login')

        else:
            print(form.errors)  # 👈 DEBUG

    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

# Login view
def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)

            if user.role == 'student':
                return redirect('student_dashboard')
            elif user.role == 'teacher':
                return redirect('teacher_dashboard')
            elif user.role == 'director':
                return redirect('director_dashboard')

        else:
            messages.error(request, "Invalid credentials")

    return render(request, 'login.html')

# Logout view
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('login')


#director dashboard view
@login_required
def director_dashboard(request):
    students = Student.objects.all()

    # ── Stat card counts ──────────────────────────────────────────
    total_students  = students.count()
    total_teachers  = Teacher.objects.count()
    total_classes   = Class.objects.count()
    pending_fees    = Fee.objects.filter(status='pending').count()
    male_students   = students.filter(gender='Male').count()
    female_students = students.filter(gender='Female').count()

    # ── Weekly attendance chart data ──────────────────────────────
    # Replace these lists with real queries from your Attendance model
    # e.g. for each day of the current week, calculate present/absent %
    attendance_labels  = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
    attendance_present = [0, 0, 0, 0, 0]   # swap with real values
    attendance_absent  = [0, 0, 0, 0, 0]   # swap with real values

    # ── Grade distribution donut data ────────────────────────────
    # Replace with real counts from your Result/Exam model
    grade_labels = ['A (Excellent)', 'B (Good)', 'C (Average)', 'D (Below Avg)', 'E (Fail)']
    grade_data   = [0, 0, 0, 0, 0]         # swap with real values

    context = {
        # Students table
        'students': students.order_by('-id')[:10],

        # Stat cards
        'total_students':  total_students,
        'total_teachers':  total_teachers,
        'total_classes':   total_classes,
        'pending_fees_count': pending_fees,

        # Quick overview
        'male_students':   male_students,
        'female_students': female_students,

        # Chart data serialised to JSON — used with |safe in template
        'attendance_labels':  json.dumps(attendance_labels,  cls=DjangoJSONEncoder),
        'attendance_present': json.dumps(attendance_present, cls=DjangoJSONEncoder),
        'attendance_absent':  json.dumps(attendance_absent,  cls=DjangoJSONEncoder),
        'grade_labels': json.dumps(grade_labels, cls=DjangoJSONEncoder),
        'grade_data':   json.dumps(grade_data,   cls=DjangoJSONEncoder),
    }
    return render(request, 'school_mgt_app/director_dashboard.html', context)


def students_view(request):
    students = Student.objects.all().order_by('-id')

    form = StudentForm()

    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('students')

    return render(request, 'students.html', {
        'students': students,
        'form': form
    })


# Dashboard views
def student_dashboard(request):
    return render(request, 'student_dashboard.html')

def teacher_dashboard(request):
    return render(request, 'teacher_dashboard.html')

def director_dashboard(request):
    return render(request, 'director_dashboard.html')