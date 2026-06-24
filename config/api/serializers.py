# ==========================================
# AI LearnMate - API Serializers
# Converts Django Models to JSON and
# JSON data to Django Models
# ==========================================

from rest_framework import serializers
from django.contrib.auth.models import User

from courses.models import Category, Course, StudyMaterial
from quizzes.models import Quiz,Question,StudentResult

# ==========================================
# AUTHENTICATION SERIALIZERS
# Handles User Registration
# ==========================================
class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:

        model = User

        fields = [
            'id',
            'first_name',
            'username',
            'email',
            'password'
        ]

        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):

        user = User.objects.create_user(

            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            password=validated_data['password']

        )

        return user

# ==========================================
# COURSE MANAGEMENT SERIALIZERS
# Handles Categories, Courses and
# Study Materials
# ==========================================


class CategorySerializer(serializers.ModelSerializer):

    class Meta:

        model = Category

        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):

    category_name = serializers.CharField(
        source='category.name',
        read_only=True
    )

    class Meta:

        model = Course

        fields = [
            'id',
            'title',
            'description',
            'duration',
            'category',
            'category_name'
        ]


class StudyMaterialSerializer(serializers.ModelSerializer):

    course_name = serializers.CharField(
        source='course.title',
        read_only=True
    )

    class Meta:

        model = StudyMaterial

        fields = '__all__'



# ==========================================
# QUIZ MANAGEMENT SERIALIZERS
# Handles Quiz, Questions and Results
# ==========================================

class QuizSerializer(serializers.ModelSerializer):

    class Meta:
        model = Quiz
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question

        exclude = ['correct_answer']

class StudentResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentResult
        fields = '__all__'