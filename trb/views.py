from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import authenticate, login
from .models import Student, Teacher, Course, QuestionPaper, ExamSchedule, ClassTimetable
from .custom_auth import StudentAuthenticationBackend
from django.contrib.auth import login, logout, authenticate
from .forms import StudentSignupForm

def student_logout(request):
    logout(request)
    return redirect('home') 

def home(request):
    return render(request, 'trb/home.html')
    
def student_signup(request):
    if request.method == 'POST':
        form = StudentSignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'],
                                            password=form.cleaned_data['password'],
                                            email=form.cleaned_data['email'])
            student = form.save(commit=False)
            student.user = user
            student.save()
            login(request, user)
            return redirect('home')
    else:
        form = StudentSignupForm()
    return render(request, 'trb/student_signup.html', {'form': form})

def student_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            student = Student.objects.filter(user=user).first()
            if student:
                login(request, user)
                if student.approved:
                    return redirect('student_home')
                else:
                    return redirect('waiting_approval')
            else:
                # Handle login for non-student users
                pass
        else:
            # Handle invalid login
            pass
    return render(request, 'trb/student_login.html')

def teacher_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            teacher = Teacher.objects.filter(user=user).first()
            if teacher:
                login(request, user)
                return redirect('teacher_home')
            else:
                # Handle login for non-teacher users
                pass
        else:
            # Handle invalid login
            pass
    return render(request, 'trb/teacher_login.html')



@login_required
def teacher_home(request):
    student_requests_count = Student.objects.filter(approved=False).count()
    all_students = Student.objects.all()
    courses = Course.objects.all()
    question_papers = QuestionPaper.objects.all()
    exam_schedule = ExamSchedule.objects.all()
    class_timetable = ClassTimetable.objects.all()
    student_requests = Student.objects.filter(approved=False)
    return render(request, 'trb/teacher_home.html', {
        'student_requests_count': student_requests_count,
        'all_students': all_students,
        'courses': courses,
        'question_papers': question_papers,
        'exam_schedule': exam_schedule,
        'class_timetable': class_timetable,
    })

@login_required
def student_requests_list(request):
    student_requests = Student.objects.filter(approved=False)
    return render(request, 'trb/student_requests_list.html', {'student_requests': student_requests})

@login_required
def approve_student(request, student_id):
    if request.method == 'POST':
        # Your existing logic for approving a student
        student = Student.objects.get(pk=student_id)
        action = request.POST.get('action')
        
        if action == 'allow':
            student.approved = True
            student.save()
            # Redirect to the appropriate URL based on the context
            if 'student_requests' in request.path:
                return redirect('student_requests_list')
            else:
                return redirect('list_student_requests')
        elif action == 'deny':
            student.delete()  # Or handle denial in your application logic
            # Redirect to the appropriate URL based on the context
            if 'student_requests' in request.path:
                return redirect('student_requests_list')
            else:
                return redirect('list_student_requests')
    else:
        return redirect('teacher_home')  # Redirect if accessed via GET request or unauthorized access

@login_required
def deny_student(request, student_id):
    if not request.user.is_authenticated or not hasattr(request.user, 'teacher'):
        return redirect('home')

    teacher = request.user.teacher
    if not teacher:
        return redirect('home')

    student = Student.objects.get(pk=student_id)
    student.delete()  # Assuming you want to delete the student
    return redirect('list_student_requests')

@login_required
def delete_student(request, student_id):
    if not request.user.is_teacher:
        return redirect('home')

    student = Student.objects.get(pk=student_id)
    student.delete()
    return redirect('approve_students')

class StudentProfileCreateView(CreateView):
    model = Student
    form_class = StudentSignupForm
    template_name = 'trb/student_profile_create.html'
    success_url = reverse_lazy('student_profile_created')

    def form_valid(self, form):
        # Check if a Student object already exists for the user
        if Student.objects.filter(user=self.request.user).exists():
            # If a Student object already exists, redirect to the homepage
            return redirect('home')  # Adjust the URL name as needed
        else:
            # If no Student object exists, create a new one
            student = form.save(commit=False)
            student.user = self.request.user
            student.save()
            return super().form_valid(form)


def student_profile_created_view(request):
    # Define your view logic for the success page here
    return render(request, 'trb/student_profile_created.html')
  
@login_required
def list_student_requests(request):
    student_requests = Student.objects.filter(approved=False)
    return render(request, 'trb/student_requests.html', {'student_requests': student_requests})

@login_required
def student_detail_requests(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    return render(request, 'trb/student_detail_requests.html', {'student': student})

@login_required
def student_details(request, student_id):
    student = Student.objects.get(pk=student_id)
    return render(request, 'trb/student_details.html', {'student': student})

@login_required
def student_home(request):
    try:
        student = request.user.student  # Retrieve the related Student object
        if not student.approved:
            # Redirect to waiting for approval page
            return render(request, 'trb/waiting_approval.html')
    except Student.DoesNotExist:
        # If the related Student object does not exist, redirect the user to create their student profile
        return redirect('student_profile_create')  # Adjust the URL name as needed

    # Continue with your view logic...
    # For example, you can pass the student object to the template:
    return render(request, 'trb/student_home.html', {'student': student})

@login_required
def students_list(request):
    students = Student.objects.all()
    return render(request, 'trb/students_list.html', {'students': students})



def edit_student(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    if request.method == 'POST':
        form = StudentSignupForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            # Redirect or show a success message
    else:
        form = StudentSignupForm(instance=student)
    return render(request, 'trb/edit_student.html', {'form': form})
    
def waiting_approval(request):
    return render(request, 'trb/waiting_approval.html')
