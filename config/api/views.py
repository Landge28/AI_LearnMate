from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from .serializers import UserRegisterSerializer
from rest_framework.authtoken.models import Token


from .serializers import (CategorySerializer,CourseSerializer,StudyMaterialSerializer)
from courses.models import Category,Course,StudyMaterial

from quizzes.models import Quiz,Question,StudentResult
from .serializers import QuizSerializer,QuestionSerializer,StudentResultSerializer

from progress_tracker.models import ProgressTracker
from .serializers import ProgressTrackerSerializer

from recommendations.models import Recommendation

from ai_tutor.services import AIService
from .serializers import AIChatSerializer

# ==========================================
# USER AUTHENTICATION APIs
# Handles User Registration
# ==========================================
class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):

        serializer = UserRegisterSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    "message": "User Registered Successfully"
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# ==========================================
# USER LOGIN API
# Authenticates User and Generates Token
# ==========================================
class LoginAPIView(APIView):

    permission_classes = []

    def post(self, request):

        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate( username=username,password=password)

        if user:

            token, created = Token.objects.get_or_create(user=user)

            return Response({

                "message": "Login Successful",

                "token": token.key,

                "username": user.username

            })

        return Response(
            {
                "error": "Invalid Credentials"
            },
            status=401
        )


# ==========================================
# USER PROFILE API
# Returns Logged-in User Details
# ==========================================
class ProfileAPIView(APIView):

    def get(self, request):

        user = request.user

        return Response({

            "id": user.id,

            "name": user.first_name,

            "username": user.username,

            "email": user.email

        })


# ==========================================
# USER LOGOUT API
# Handles User Logout
# ==========================================
class LogoutAPIView(APIView):

    def post(self, request):

        return Response({
            "message": "Logout Successful"
        })



# ==========================================
# CATEGORY MANAGEMENT API
# Returns All Course Categories
# ==========================================
class CategoryListAPIView(APIView):

    permission_classes = [AllowAny]
    def get(self, request):
        categories = Category.objects.all()

        serializer = CategorySerializer(categories,many=True)

        return Response(serializer.data)




# ==========================================
# COURSE MANAGEMENT API
# Returns All Available Courses
# ==========================================
class CourseListAPIView(APIView):

    permission_classes = [AllowAny]
    def get(self, request):
        courses = Course.objects.all()

        serializer = CourseSerializer(courses,many=True)

        return Response(serializer.data)




# ==========================================
# COURSE DETAILS API
# Returns Details of a Selected Course
# ==========================================
class CourseDetailAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, pk):

        try:

            course = Course.objects.get(id=pk)

            serializer = CourseSerializer(course)

            return Response(serializer.data)

        except Course.DoesNotExist:

            return Response(
                {
                    "error": "Course Not Found"
                },
                status=404
            )




# ==========================================
# STUDY MATERIAL API
# Returns Study Materials for Courses
# ==========================================
class StudyMaterialAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):

        materials = StudyMaterial.objects.all()

        serializer = StudyMaterialSerializer(materials,many=True)

        return Response(serializer.data)





# ==========================================
# QUIZ MANAGEMENT API
# Returns All Available Quizzes
# ==========================================
class QuizListAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        quizzes = Quiz.objects.all()

        serializer = QuizSerializer(quizzes,many=True)

        return Response(serializer.data)






# ==========================================
# QUIZ QUESTION API
# Returns Questions for a Selected Quiz
# ==========================================
class QuizQuestionAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, quiz_id):

        questions = Question.objects.filter(quiz_id=quiz_id)

        serializer = QuestionSerializer(questions,many=True)

        return Response(serializer.data)






# ==========================================
# QUIZ SUBMISSION API
# Evaluates Quiz and Updates Student Progress
# ==========================================
class SubmitQuizAPIView(APIView):

    def post(self, request):

        quiz_id = request.data.get('quiz_id')

        answers = request.data.get('answers')

        questions = Question.objects.filter(quiz_id=quiz_id)

        score = 0

        for question in questions:

            submitted_answer = answers.get(str(question.id))

            if submitted_answer == question.correct_answer:

                score += 1

        result = StudentResult.objects.create(student=request.user,quiz_id=quiz_id,score=score)

        all_results = StudentResult.objects.filter(student=request.user)

        total_attempts = all_results.count()

        average_score = sum(r.score for r in all_results) / total_attempts

        highest_score = max(r.score for r in all_results)

        progress_percentage = (average_score / questions.count()) * 100

        progress, created = (ProgressTracker.objects.get_or_create(student=request.user))

        progress.quizzes_attempted = total_attempts

        progress.average_score = average_score

        progress.highest_score = highest_score

        progress.progress_percentage = (progress_percentage)

        progress.save()

        return Response(
            {
                "message": "Quiz Submitted Successfully",
                "score": score,
                "progress": progress.progress_percentage
            },
            status=status.HTTP_200_OK
        )





# ==========================================
# PROGRESS TRACKER API
# Returns Student Learning Progress
# ==========================================
class ProgressAPIView(APIView):

    def get(self, request):

        try:

            progress = ProgressTracker.objects.get(student=request.user)

            serializer = ProgressTrackerSerializer(progress)

            return Response(serializer.data)

        except ProgressTracker.DoesNotExist:

            return Response(
                {
                    "message":
                    "No Progress Data Found"
                },
                status=404
            )


# ==========================================
# RECOMMENDATION API
# Fetches AI-based personalized course
# recommendations for the logged-in student
# ==========================================

class RecommendationAPIView(APIView):
    def get(self, request):

        try:

            progress = ProgressTracker.objects.get(student=request.user)

            if progress.progress_percentage < 50:

                courses = Course.objects.all()[:3]

                reason = "Beginner Level Recommended"

            elif progress.progress_percentage < 75:

                courses = Course.objects.all()[:3]

                reason = "Intermediate Level Recommended"

            else:

                courses = Course.objects.all()[:3]

                reason = "Advanced Level Recommended"

            recommendations = []

            for course in courses:

                recommendations.append({

                    "course": course.title,

                    "reason": reason

                })

            return Response(recommendations)

        except ProgressTracker.DoesNotExist:

            return Response({

                "message":
                "No Progress Found"

            })


# ============================================
# AI Tutor API
# Receives student questions and returns
# AI-generated learning assistance
# ============================================
class AIChatAPIView(APIView):

    def post(self, request):

        serializer = AIChatSerializer(data=request.data)

        if serializer.is_valid():

            question = serializer.validated_data["question"]

            ai = AIService()

            answer = ai.ask_ai(question)

            return Response({

                "question": question,

                "answer": answer

            })

        return Response(serializer.errors,status=400)