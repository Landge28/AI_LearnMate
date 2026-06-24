from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from .serializers import UserRegisterSerializer
from rest_framework.authtoken.models import Token


from .serializers import (CategorySerializer,CourseSerializer,StudyMaterialSerializer)
from rest_framework.permissions import AllowAny

from courses.models import Category,Course,StudyMaterial

from quizzes.models import Quiz,Question,StudentResult

from .serializers import QuizSerializer,QuestionSerializer,StudentResultSerializer


class RegisterAPIView(APIView):

    permission_classes = []

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


class LoginAPIView(APIView):

    permission_classes = []

    def post(self, request):

        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(
            username=username,
            password=password
        )

        if user:

            token, created = Token.objects.get_or_create(
                user=user
            )

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

class ProfileAPIView(APIView):

    def get(self, request):

        user = request.user

        return Response({

            "id": user.id,

            "name": user.first_name,

            "username": user.username,

            "email": user.email

        })


class LogoutAPIView(APIView):

    def post(self, request):

        return Response({
            "message": "Logout Successful"
        })




class CategoryListAPIView(APIView):

    permission_classes = [AllowAny]
    def get(self, request):
        categories = Category.objects.all()

        serializer = CategorySerializer(
            categories,
            many=True
        )

        return Response(serializer.data)


class CourseListAPIView(APIView):

    permission_classes = [AllowAny]
    def get(self, request):
        courses = Course.objects.all()

        serializer = CourseSerializer(
            courses,
            many=True
        )

        return Response(serializer.data)


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

class StudyMaterialAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):

        materials = StudyMaterial.objects.all()

        serializer = StudyMaterialSerializer(
            materials,
            many=True
        )

        return Response(serializer.data)


from rest_framework.permissions import AllowAny

class QuizListAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        quizzes = Quiz.objects.all()

        serializer = QuizSerializer(
            quizzes,
            many=True
        )

        return Response(serializer.data)


class QuizQuestionAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, quiz_id):

        questions = Question.objects.filter(
            quiz_id=quiz_id
        )

        serializer = QuestionSerializer(
            questions,
            many=True
        )

        return Response(serializer.data)


class SubmitQuizAPIView(APIView):

    def post(self, request):

        quiz_id = request.data.get('quiz_id')

        answers = request.data.get('answers')

        questions = Question.objects.filter(
            quiz_id=quiz_id
        )

        score = 0

        for question in questions:

            submitted_answer = answers.get(
                str(question.id)
            )

            if submitted_answer == question.correct_answer:

                score += 1

        StudentResult.objects.create(

            student=request.user,

            quiz_id=quiz_id,

            score=score

        )

        return Response({

            "message": "Quiz Submitted",

            "score": score,

            "total_questions": questions.count()

        })