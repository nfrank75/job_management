from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import User, Student, Company, Internship, Application

@api_view(['POST'])
def register(request):
    try:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user_type = request.POST.get('user_type')
                if user_type == 'student':
                    user.is_student = True
                    first_name = request.POST.get('first_name')
                    last_name = request.POST.get('last_name')
                    academic_level = request.POST.get('academic_level')
                    phone = request.POST.get('phone')
                    cv = request.FILES.get('cv')
                    transcript = request.FILES.get('transcript')
                    student = Student.objects.create(
                        user=user,
                        first_name=first_name,
                        last_name=last_name,
                        academic_level=academic_level,
                        phone=phone,
                        cv=cv,
                        transcript=transcript
                    )
                elif user_type == 'company':
                    user.is_company = True
                    name = request.POST.get('name')
                    description = request.POST.get('description')
                    website = request.POST.get('website')
                    contact_person = request.POST.get('contact_person')
                    contact_email = request.POST.get('contact_email')
                    company = Company.objects.create(
                        user=user,
                        name=name,
                        description=description,
                        website=website,
                        contact_person=contact_person,
                        contact_email=contact_email
                    )
                user.save()
                login(request, user)
                return redirect('dashboard')
        else:
            form = UserCreationForm()
        return render(request, 'register.html', {'form': form})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_view(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_student:
                    return redirect('student_dashboard')
                elif user.is_company:
                    return redirect('company_dashboard')
                else:
                    return redirect('dashboard')
            else:
                return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
        return render(request, 'login.html')
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_internship(request):
    try:
        if request.method == 'POST':
            title = request.POST.get('title')
            description = request.POST.get('description')
            location = request.POST.get('location')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            requirements = request.POST.get('requirements')
            company = Company.objects.get(user=request.user)
            internship = Internship.objects.create(
                title=title,
                description=description,
                location=location,
                start_date=start_date,
                end_date=end_date,
                requirements=requirements,
                company=company
            )
            return redirect('company_dashboard')
        return render(request, 'post_internship.html')
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def manage_applications(request, internship_id):
    try:
        internship = Internship.objects.get(id=internship_id)
        applications = internship.applications.all()
        if request.method == 'POST':
            application_id = request.POST.get('application_id')
            status = request.POST.get('status')
            application = Application.objects.get(id=application_id)
            application.status = status
            application.save()
        return render(request, 'manage_applications.html', {'internship': internship, 'applications': applications})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def student_dashboard(request):
    try:
        student = Student.objects.get(user=request.user)
        internships = Internship.objects.all()
        applications = student.applications.all()
        return render(request, 'student_dashboard.html', {'student': student, 'internships': internships, 'applications': applications})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def company_dashboard(request):
    try:
        company = Company.objects.get(user=request.user)
        internships = company.internships.all()
        applications = Application.objects.filter(internship__in=internships)
        return render(request, 'company_dashboard.html', {'company': company, 'internships': internships, 'applications': applications})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def apply_for_internship(request, internship_id):
    try:
        internship = Internship.objects.get(id=internship_id)
        student = Student.objects.get(user=request.user)
        application = Application.objects.create(student=student, internship=internship)
        return redirect('student_dashboard')
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)