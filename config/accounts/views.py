from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect

from django.contrib.auth.models import User

from django.contrib.auth import authenticate,login,logout

from .forms import UserRegisterForm
from courses.models import Course, StudyMaterial
from quizzes.models import Quiz
from progress_tracker.models import ProgressTracker
from recommendations.models import Recommendation

from .models import StudentProfile

from django.contrib.auth.decorators import login_required

from quizzes.models import StudentResult

from courses.models import Course

from .forms import StudentProfileForm

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


# ==========================================
# ACCOUNTS APP - USER AUTHENTICATION VIEWS
# Handles user registration, login, logout
# and profile-related operations
# ==========================================


# ==========================================
# HOME PAGE VIEW
# Displays application home page
# ==========================================
def home(request):
    return render(request, 'home.html')



# ==========================================
# USER REGISTRATION VIEW
# Creates a new user account
# ==========================================
def register_view(request):
    if request.method == 'POST':

        form = UserRegisterForm(request.POST)

        if form.is_valid():

            user = User.objects.create_user(

                first_name=form.cleaned_data['first_name'],


                username=form.cleaned_data['username'],

                email=form.cleaned_data['email'],


                password=form.cleaned_data['password']

            )

            user.save()

            return redirect('login')

    else:

        form = UserRegisterForm()

    return render(request,'accounts/register.html',{'form': form})



# ==========================================
# USER LOGIN VIEW
# Authenticates user credentials
# ==========================================
def login_view(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request,username=username,password=password)

        if user:

            login(request, user)

            response = redirect('dashboard')

            response.set_cookie('username',username,max_age=86400)

            return response

        return render(request,'accounts/login.html',{'error': 'Invalid Credentials'})

    return render(request,'accounts/login.html')



# ==========================================
# USER DASHBOARD VIEW
# Displays dashboard for authenticated users
# Redirects unauthenticated users to login page
# ==========================================


# def dashboard_view(request):
#
#     if not request.user.is_authenticated:
#
#         return redirect('login')
#
#     return render(request,'accounts/dashboard.html')
# @login_required
# def dashboard_view(request):
#
#     user = request.user
#
#     total_courses = Course.objects.count()
#
#     total_quizzes = Quiz.objects.count()
#
#     progress = ProgressTracker.objects.filter(student=user).first()
#
#     total_recommendations = Recommendation.objects.filter(student=user).count()
#
#     context = {
#
#         "total_courses": total_courses,
#         "total_materials": total_materials,
#         "total_quizzes": total_quizzes,
#         "recommendations": total_recommendations,
#         "progress": progress,
#
#         # User Details
#         "user": request.user,
#
#     }
#
#     return render(
#         request,
#         "accounts/dashboard.html",
#         context,
#     )
@login_required
def dashboard_view(request):

    user = request.user

    total_courses = Course.objects.count()

    total_materials = StudyMaterial.objects.count()

    total_quizzes = Quiz.objects.count()

    latest_course = Course.objects.order_by("-created_at").first()

    total_recommendations = Recommendation.objects.filter(student=user).count()

    progress = ProgressTracker.objects.filter(student=user).first()

    recent_courses = Course.objects.order_by("-created_at")[:5]

    context = {

        "total_courses": total_courses,
        "total_materials": total_materials,
        "total_quizzes": total_quizzes,
        "recommendations": total_recommendations,
        "progress": progress,
        "latest_course": latest_course,
        "recent_courses": recent_courses,

    }

    return render(
        request,
        "accounts/dashboard.html",
        context
    )
# ==========================================
# USER LOGOUT VIEW
# Logs out the current user
# Clears session and username cookie
# Redirects user to login page
# ==========================================
def logout_view(request):

    logout(request)

    response = redirect('login')

    response.delete_cookie('username')

    return response

@login_required
def profile(request):

    user = request.user

    # Get or create student profile
    profile, created = StudentProfile.objects.get_or_create(
        user=user
    )

    # Progress
    progress = ProgressTracker.objects.filter(
        student=user
    ).first()

    # Quiz Attempts
    quiz_attempts = StudentResult.objects.filter(
        student=user
    ).count()

    # Total Courses
    total_courses = Course.objects.count()

    context = {

        "user": user,

        "profile": profile,

        "progress": progress,

        "quiz_attempts": quiz_attempts,

        "total_courses": total_courses,

    }

    return render(
        request,
        "accounts/profile.html",
        context
    )

@login_required
def edit_profile(request):

    profile, created = StudentProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        form = StudentProfileForm(

            request.POST,

            request.FILES,

            instance=profile

        )

        if form.is_valid():

            form.save()

            return redirect("profile")

    else:

        form = StudentProfileForm(instance=profile)

    return render(

        request,

        "accounts/edit_profile.html",

        {

            "form": form

        }

    )

@login_required
def change_password(request):

    if request.method == "POST":

        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():

            user = form.save()

            update_session_auth_hash(request, user)

            print("SUCCESS")

            return redirect("change_password_donepython manage.py runserver")

        else:

            print(form.errors)

    else:

        form = PasswordChangeForm(request.user)

    return render(
        request,
        "accounts/change_password.html",
        {
            "form": form
        }
    )

@login_required
def change_password_done(request):

    return render(
        request,
        "accounts/change_password_done.html"
    )