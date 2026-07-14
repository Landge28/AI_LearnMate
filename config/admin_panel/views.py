from django.shortcuts import render,redirect
from django.contrib.admin.views.decorators import staff_member_required

from django.contrib.auth.models import User
from courses.models import Course, StudyMaterial, Certificate
from quizzes.models import Quiz
from django.contrib.auth.models import User

from accounts.models import StudentProfile
from .forms import StudentAdminForm, StudentProfileAdminForm
import json
from django.db.models.functions import TruncMonth
from django.db.models import Count

from courses.models import Course

from .forms import CourseForm

from courses.models import StudyMaterial

from .forms import StudyMaterialForm

from django.shortcuts import get_object_or_404
from quizzes.models import Quiz
from .forms import QuizForm

from quizzes.models import Question
from .forms import QuestionForm
from quizzes.models import StudentResult
from progress_tracker.models import ProgressTracker
from ai_tutor.models import ChatSession

from courses.models import Certificate
from accounts.models import Notification
from .forms import NotificationForm


@staff_member_required
def admin_dashboard(request):
    student_labels = [
        "Students",
        "Courses",
        "Quizzes",
        "Certificates",
    ]

    student_values = [

        User.objects.filter(is_staff=False).count(),

        Course.objects.count(),

        Quiz.objects.count(),

        Certificate.objects.count(),

    ]

    monthly_students = (

        User.objects
        .filter(is_staff=False)
        .annotate(month=TruncMonth("date_joined"))
        .values("month")
        .annotate(total=Count("id"))
        .order_by("month")

    )

    months = []

    student_counts = []

    for item in monthly_students:
        months.append(item["month"].strftime("%b %Y"))

        student_counts.append(item["total"])

    context = {

        "students": User.objects.filter(is_staff=False).count(),

        "courses": Course.objects.count(),

        "materials": StudyMaterial.objects.count(),

        "quizzes": Quiz.objects.count(),

        "certificates": Certificate.objects.count(),

        "chart_labels": json.dumps(student_labels),

        "chart_values": json.dumps(student_values),

        "context_months": json.dumps(months),

        "context_student_counts": json.dumps(student_counts),

    }

    return render(request,"admin_panel/dashboard.html",context,)


@staff_member_required
def students(request):

    students = User.objects.filter(is_staff=False).order_by("-date_joined")

    return render(
        request,
        "admin_panel/students.html",
        {
            "students": students
        }
    )

@staff_member_required
def student_detail(request, user_id):

    student = get_object_or_404(User,id=user_id)

    profile, created = StudentProfile.objects.get_or_create(user=student)

    return render(
        request,
        "admin_panel/student_detail.html",
        {
            "student": student,
            "profile": profile,
        }
    )

@staff_member_required
def edit_student(request, user_id):

    student = get_object_or_404(User,id=user_id)

    profile, created = StudentProfile.objects.get_or_create(user=student)

    if request.method == "POST":

        user_form = StudentAdminForm(request.POST,instance=student)

        profile_form = StudentProfileAdminForm(request.POST,request.FILES,instance=profile)

        if user_form.is_valid() and profile_form.is_valid():

            user_form.save()
            profile_form.save()

            return redirect(
                "student_detail",
                user_id=student.id
            )

    else:

        user_form = StudentAdminForm(instance=student)
        profile_form = StudentProfileAdminForm(instance=profile)

    return render(
        request,
        "admin_panel/edit_student.html",
        {
            "student": student,
            "user_form": user_form,
            "profile_form": profile_form,
        },
    )

@staff_member_required
def delete_student(request, user_id):

    student = get_object_or_404(User,id=user_id)

    # Never allow deleting superusers
    if student.is_superuser:
        return redirect("admin_students")

    if request.method == "POST":
        student.delete()
        return redirect("admin_students")

    return render(
        request,
        "admin_panel/delete_student.html",
        {
            "student": student
        }
    )

@staff_member_required
def courses(request):

    courses = Course.objects.select_related("category").order_by("-created_at")

    return render(
        request,
        "admin_panel/courses.html",
        {
            "courses": courses
        }
    )

@staff_member_required
def add_course(request):

    if request.method == "POST":

        form = CourseForm(request.POST,request.FILES)

        if form.is_valid():

            form.save()

            return redirect("admin_courses")

    else:

        form = CourseForm()

    return render(
        request,
        "admin_panel/add_course.html",
        {
            "form": form
        }
    )

@staff_member_required
def edit_course(request, course_id):

    course = get_object_or_404(Course,id=course_id)

    if request.method == "POST":

        form = CourseForm(request.POST,request.FILES,instance=course)

        if form.is_valid():

            form.save()

            return redirect("admin_courses")

    else:

        form = CourseForm(instance=course)

    return render(
        request,
        "admin_panel/edit_course.html",
        {
            "form": form,
            "course": course
        }
    )

@staff_member_required
def delete_course(request, course_id):

    course = get_object_or_404(Course,id=course_id)

    if request.method == "POST":

        course.delete()

        return redirect("admin_courses")

    return render(
        request,
        "admin_panel/delete_course.html",
        {
            "course": course
        }
    )

@staff_member_required
def materials(request):

    materials = StudyMaterial.objects.select_related("course").order_by("-id")

    return render(
        request,
        "admin_panel/materials.html",
        {
            "materials": materials
        }
    )

@staff_member_required
def add_material(request):

    if request.method == "POST":

        form = StudyMaterialForm(request.POST,request.FILES)

        if form.is_valid():

            form.save()

            return redirect("admin_materials")

    else:

        form = StudyMaterialForm()

    return render(
        request,
        "admin_panel/add_material.html",
        {
            "form": form
        }
    )

@staff_member_required
def edit_material(request, pk):

    material = get_object_or_404(StudyMaterial,pk=pk)

    if request.method == "POST":

        form = StudyMaterialForm(request.POST,request.FILES,instance=material)

        if form.is_valid():

            form.save()

            return redirect("admin_materials")

    else:

        form = StudyMaterialForm(
            instance=material
        )

    return render(
        request,
        "admin_panel/edit_material.html",
        {
            "form": form
        }
    )

@staff_member_required
def delete_material(request, pk):

    material = get_object_or_404(StudyMaterial,pk=pk)

    material.delete()

    return redirect("admin_materials")


@staff_member_required
def admin_quizzes(request):

    quizzes = Quiz.objects.select_related("course")

    return render(
        request,
        "admin_panel/quizzes.html",
        {
            "quizzes": quizzes
        }
    )

@staff_member_required
def add_quiz(request):

    if request.method == "POST":

        form = QuizForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("admin_quizzes")

    else:

        form = QuizForm()

    return render(
        request,
        "admin_panel/add_quiz.html",
        {
            "form": form
        }
    )

@staff_member_required
def edit_quiz(request, quiz_id):

    quiz = get_object_or_404(Quiz,id=quiz_id)

    if request.method == "POST":

        form = QuizForm(request.POST,instance=quiz)

        if form.is_valid():

            form.save()

            return redirect("admin_quizzes")

    else:

        form = QuizForm(instance=quiz)

    return render(
        request,
        "admin_panel/edit_quiz.html",
        {
            "form": form,
            "quiz": quiz,
        }
    )



@staff_member_required
def delete_quiz(request, quiz_id):

    quiz = get_object_or_404(Quiz,id=quiz_id)

    if request.method == "POST":

        quiz.delete()

        return redirect("admin_quizzes")

    return render(
        request,
        "admin_panel/delete_quiz.html",
        {
            "quiz": quiz,
        }
    )


@staff_member_required
def admin_questions(request, quiz_id):

    quiz = get_object_or_404(Quiz,id=quiz_id)

    questions = Question.objects.filter(quiz=quiz)

    return render(
        request,
        "admin_panel/questions.html",
        {
            "quiz": quiz,
            "questions": questions,
        }
    )

@staff_member_required
def add_question(request, quiz_id):

    quiz = get_object_or_404(Quiz,id=quiz_id)

    if request.method == "POST":

        form = QuestionForm(request.POST)

        if form.is_valid():

            question = form.save(commit=False)

            question.quiz = quiz

            question.save()

            return redirect(
                "admin_questions",
                quiz_id=quiz.id
            )

    else:

        form = QuestionForm()

    return render(
        request,
        "admin_panel/add_question.html",
        {
            "quiz": quiz,
            "form": form,
        }
    )


@staff_member_required
def edit_question(request, question_id):

    question = get_object_or_404(Question,id=question_id)

    if request.method == "POST":

        form = QuestionForm(request.POST,instance=question)

        if form.is_valid():

            form.save()

            return redirect("admin_questions",quiz_id=question.quiz.id)

    else:

        form = QuestionForm(instance=question)

    return render(
        request,
        "admin_panel/edit_question.html",
        {
            "form": form,
            "question": question,
        }
    )

@staff_member_required
def delete_question(request, question_id):

    question = get_object_or_404(Question,id=question_id)

    quiz_id = question.quiz.id

    if request.method == "POST":

        question.delete()

        return redirect("admin_questions",quiz_id=quiz_id)

    return render(
        request,
        "admin_panel/delete_question.html",
        {
            "question": question,
        }
    )

@staff_member_required
def student_results(request):

    results = StudentResult.objects.select_related(
        "student",
        "quiz",
        "quiz__course"
    )

    search = request.GET.get("search")

    if search:

        results = results.filter(student__username__icontains=search)

    course = request.GET.get("course")

    if course:

        results = results.filter(quiz__course_id=course)

    quiz = request.GET.get("quiz")

    if quiz:

        results = results.filter(quiz_id=quiz)

    context = {

        "results": results.order_by("-attempted_at"),

        "courses": Course.objects.all(),

        "quizzes": Quiz.objects.all(),

    }

    return render(
        request,
        "admin_panel/student_results.html",
        context
    )

@staff_member_required
def progress_management(request):
    progress = ProgressTracker.objects.select_related("student")

    search = request.GET.get("search")

    if search:
        progress = progress.filter(student__username__icontains=search)

    progress = progress.order_by("-progress_percentage")

    return render(
        request,
        "admin_panel/progress_management.html",
        {
            "progress": progress
        }
    )

@staff_member_required
def ai_chat_sessions(request):

    sessions = (
        ChatSession.objects
        .select_related("student")
        .prefetch_related("messages")
        .order_by("-created_at")
    )

    return render(
        request,
        "admin_panel/ai_chat_sessions.html",
        {
            "sessions": sessions
        }
    )


@staff_member_required
def chat_detail(request, session_id):

    session = get_object_or_404(
        ChatSession.objects.select_related("student"),
        id=session_id
    )

    messages = session.messages.all().order_by("created_at")

    return render(
        request,
        "admin_panel/chat_detail.html",
        {
            "session": session,
            "messages": messages,
        },
    )

@staff_member_required
def delete_chat_session(request, session_id):

    session = get_object_or_404(ChatSession,id=session_id)

    session.delete()

    return redirect("admin_ai_chat")

@staff_member_required
def ai_chat_sessions(request):

    sessions = ChatSession.objects.select_related("student").prefetch_related("messages")

    search = request.GET.get("search")

    if search:

        sessions = sessions.filter(student__username__icontains=search)

    sessions = sessions.order_by("-created_at")

    return render(
        request,
        "admin_panel/ai_chat_sessions.html",
        {
            "sessions": sessions
        }
    )

@staff_member_required
def certificates(request):

    certificates = (
        Certificate.objects
        .select_related("student", "course")
        .order_by("-issued_at")
    )

    return render(
        request,
        "admin_panel/certificates.html",
        {
            "certificates": certificates
        }
    )

@staff_member_required
def notifications(request):

    notifications = Notification.objects.order_by("-created_at")

    return render(
        request,
        "admin_panel/notifications.html",
        {
            "notifications": notifications
        }
    )

@staff_member_required
def add_notification(request):

    if request.method == "POST":

        form = NotificationForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("admin_notifications")

    else:

        form = NotificationForm()

    return render(

        request,

        "admin_panel/add_notification.html",

        {

            "form": form

        }

    )

@staff_member_required
def edit_notification(request, notification_id):

    notification = get_object_or_404(
        Notification,
        id=notification_id
    )

    if request.method == "POST":

        form = NotificationForm(
            request.POST,
            instance=notification
        )

        if form.is_valid():

            form.save()

            return redirect("admin_notifications")

    else:

        form = NotificationForm(
            instance=notification
        )

    return render(
        request,
        "admin_panel/edit_notification.html",
        {
            "form": form
        }
    )


@staff_member_required
def delete_notification(request, notification_id):

    notification = get_object_or_404(
        Notification,
        id=notification_id
    )

    if request.method == "POST":

        notification.delete()

        return redirect("admin_notifications")

    return render(
        request,
        "admin_panel/delete_notification.html",
        {
            "notification": notification
        }
    )