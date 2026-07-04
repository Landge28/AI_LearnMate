from django.urls import path
from . import views

urlpatterns = [

    path("",views.ai_tutor_page,name="ai_tutor"),

]