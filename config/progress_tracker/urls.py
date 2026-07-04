from django.urls import path
from . import views

urlpatterns = [

    path("",views.progress_tracker,name="progress_tracker"),

]