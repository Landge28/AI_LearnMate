from django.urls import path
from . import views

urlpatterns = [

    path('register/', views.RegisterAPIView.as_view()),
    path('login/', views.LoginAPIView.as_view()),
    path('profile/', views.ProfileAPIView.as_view()),
    path('logout/', views.LogoutAPIView.as_view()),


    path('categories/',views.CategoryListAPIView.as_view()),

    path('courses/',views.CourseListAPIView.as_view()),

    path('courses/<int:pk>/',views.CourseDetailAPIView.as_view()),

    path('materials/',views.StudyMaterialAPIView.as_view()),


    path('quizzes/',views.QuizListAPIView.as_view()),

    path('quizzes/<int:quiz_id>/questions/',views.QuizQuestionAPIView.as_view()),

    path('submit-quiz/',views.SubmitQuizAPIView.as_view()),

]