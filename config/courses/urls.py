from django.urls import path
from . import views

urlpatterns = [

    path("", views.course_list, name="course_list"),
    path("<int:pk>/",views.course_detail,name="course_detail"),
    path("study-materials/",views.study_material_list,name="study_material_list"),
    path("materials/<int:pk>/",views.material_detail,name="material_detail"),

]