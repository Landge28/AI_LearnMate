from django import forms
from django.contrib.auth.models import User
from accounts.models import StudentProfile
from courses.models import Course
from courses.models import StudyMaterial

from quizzes.models import Quiz
from quizzes.models import Question
from accounts.models import Notification
class StudentAdminForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "is_active",
        ]


class StudentProfileAdminForm(forms.ModelForm):

    class Meta:
        model = StudentProfile
        fields = [
            "profile_image",
            "phone",
            "location",
            "bio",
            "learning_goal",
        ]



class CourseForm(forms.ModelForm):

    class Meta:

        model = Course

        fields = [
            "category",
            "title",
            "description",

        ]

        widgets = {

            "description": forms.Textarea(
                attrs={"rows": 5}
            )

        }



from courses.models import StudyMaterial


class StudyMaterialForm(forms.ModelForm):

    class Meta:

        model = StudyMaterial

        fields = [

            "course",

            "title",

            "pdf_file",
            "video_url",

        ]

        widgets = {

            "content": forms.Textarea(
                attrs={
                    "rows": 6
                }
            )

        }


class QuizForm(forms.ModelForm):

    class Meta:

        model = Quiz

        fields = [
            "course",
            "title",
            "total_marks",
        ]




class QuestionForm(forms.ModelForm):

    class Meta:

        model = Question

        fields = [

            "question_text",

            "option_a",

            "option_b",

            "option_c",

            "option_d",

            "correct_answer",

        ]

        widgets = {

            "question_text": forms.Textarea(
                attrs={
                    "rows": 4
                }
            )

        }




class NotificationForm(forms.ModelForm):

    class Meta:

        model = Notification

        fields = [

            "title",

            "message",

            "is_active",

        ]

        widgets = {

            "message": forms.Textarea(
                attrs={
                    "rows": 5
                }
            )

        }