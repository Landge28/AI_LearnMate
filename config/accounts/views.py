from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect

from django.contrib.auth.models import User

from django.contrib.auth import authenticate,login,logout

from .forms import UserRegisterForm

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


def dashboard_view(request):

    if not request.user.is_authenticated:

        return redirect('login')

    return render(request,'accounts/dashboard.html')

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

