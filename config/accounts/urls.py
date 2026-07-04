
# ==========================================
# AI LearnMate - Accounts URLs
# Authentication & User Management Routes
# ==========================================

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy


# ==========================================
# Account URL Patterns
# ==========================================
urlpatterns = [

    path('', views.home),

    path('register/', views.register_view,name='register'),
    path('login/', views.login_view,name='login'),
    path('dashboard/', views.dashboard_view,name='dashboard'),
    path('logout/', views.logout_view,name='logout'),
    path("profile/",views.profile,name="profile"),
    path("edit-profile/",views.edit_profile,name="edit_profile"),





    path("change-password/",views.change_password,name="change_password",),

    path("change-password/done/",views.change_password_done,name="change_password_done",),
]
