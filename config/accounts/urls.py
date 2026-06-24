
# ==========================================
# AI LearnMate - Accounts URLs
# Authentication & User Management Routes
# ==========================================

from django.urls import path
from . import views

# ==========================================
# Account URL Patterns
# ==========================================
urlpatterns = [

    path('', views.home),

    path('register/', views.register_view,name='register'),
    path('login/', views.login_view,name='login'),
    path('dashboard/', views.dashboard_view,name='dashboard'),
    path('logout/', views.logout_view,name='logout'),
]
