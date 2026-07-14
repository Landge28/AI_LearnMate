from django.urls import path
from . import views

urlpatterns = [

    path("", views.course_list, name="course_list"),
    path("<int:pk>/",views.course_detail,name="course_detail"),
    path("study-materials/",views.study_material_list,name="study_material_list"),
    path("materials/<int:pk>/",views.material_detail,name="material_detail"),

    path("certificate/<int:course_id>/",views.download_certificate,name="download_certificate",),

    path("<int:pk>/",views.course_detail,name="course_detail",),

    path("certificate/<int:course_id>/",views.download_certificate,name="download_certificate",),


    path("verify/<str:certificate_id>/",views.verify_certificate,name="verify_certificate",),

    path("certificate/view/<str:certificate_id>/",views.view_certificate_pdf,name="view_certificate_pdf",),

]