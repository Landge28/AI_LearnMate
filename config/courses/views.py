from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from quizzes.models import Quiz
from .models import StudyMaterial

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Course

from quizzes.models import Quiz, StudentResult
from django.contrib import messages

from reportlab.lib.enums import TA_CENTER
from reportlab.lib.colors import darkblue, grey
from reportlab.lib.styles import ParagraphStyle


from reportlab.platypus import Image
from django.conf import settings
import os
from django.shortcuts import get_object_or_404

from .models import Certificate

import qrcode
from io import BytesIO
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import landscape, A4

from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

def course_list(request):

    courses = Course.objects.select_related("category").all()

    return render(
        request,
        "courses/course_list.html",
        {
            "courses": courses
        }
    )



def course_detail(request, pk):

    course = get_object_or_404(Course,pk=pk)

    materials = course.materials.all()

    quizzes = Quiz.objects.filter(course=course)

    context = {

        "course": course,
        "materials": materials,
        "quizzes": quizzes,

    }

    return render(

        request,

        "courses/course_detail.html",

        context

    )




def study_material_list(request):

    materials = StudyMaterial.objects.select_related("course").all()

    return render(
        request,
        "courses/study_material_list.html",
        {
            "materials": materials
        }
    )


def material_detail(request, pk):

    material = get_object_or_404(
        StudyMaterial,
        pk=pk
    )

    return render(
        request,
        "courses/material_detail.html",
        {
            "material": material
        }
    )

@login_required
def download_certificate(request, course_id):

    course = get_object_or_404(Course,id=course_id)

    # Get quiz for this course
    quiz = Quiz.objects.filter(course=course).first()
    print("Course ID:", course.id)
    print("Quiz:", quiz)



    # if not quiz:
    #     messages.error(request,"No quiz is available for this course.")
    #
    #     return redirect("course_detail", course_id=course.id)

    if not quiz:
        return HttpResponse("No quiz found for this course.")
    # Get student's latest result
    result = StudentResult.objects.filter(student=request.user,quiz=quiz).order_by("-attempted_at").first()
    print("User:", request.user)
    print("Result:", result)



    # if not result:
    #     messages.error(request,"You must complete the quiz before downloading the certificate.")
    #
    #     return redirect("course_detail", course_id=course.id)

    if not result:
        return HttpResponse("Student has not attempted the quiz.")
    # Passing rule (60%)
    # passing_score = quiz.total_marks * 0.60
    total_questions = quiz.question_set.count()
    passing_score = total_questions * 0.60

    # if result.score < passing_score:
    #     messages.error(
    #         request,
    #         f"You scored {result.score}/{quiz.total_marks}. "
    #         "You must score at least 60% to download the certificate."
    #     )
    #
    #     return redirect("course_detail", pk=course.id)

    if result.score < passing_score:
        return HttpResponse(
            f"Failed. Score: {result.score}/{quiz.total_marks}"
        )

    response = HttpResponse(content_type="application/pdf")

    response["Content-Disposition"] = (f'attachment; filename="{course.title}_certificate.pdf"')

    document = SimpleDocTemplate(
        response,
        pagesize=landscape(A4),
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "Title",
        parent=styles["Title"],
        alignment=TA_CENTER,
        textColor=darkblue,
        fontSize=28,
        spaceAfter=25,
    )

    heading_style = ParagraphStyle(
        "Heading",
        parent=styles["Heading1"],
        alignment=TA_CENTER,
        fontSize=22,
        spaceAfter=20,
    )

    normal_style = ParagraphStyle(
        "Normal",
        parent=styles["BodyText"],
        alignment=TA_CENTER,
        fontSize=14,
        leading=28,
    )

    name_style = ParagraphStyle(
        "Name",
        parent=styles["Heading1"],
        alignment=TA_CENTER,
        fontSize=30,
        textColor=darkblue,
        spaceAfter=20,
    )

    story = []

    logo_path = os.path.join(
        settings.MEDIA_ROOT,
        "certificate",
        "logo.png"
    )

    if os.path.exists(logo_path):
        logo = Image(
            logo_path,
            width=80,
            height=80
        )

        logo.hAlign = "CENTER"

        story.append(logo)


    story.append(
        Paragraph(
            "AI LearnMate",
            title_style
        )
    )

    story.append(
        Paragraph(
            "CERTIFICATE OF COMPLETION",
            heading_style
        )
    )

    story.append(
        Paragraph(
            "This Certificate is Proudly Awarded To",
            normal_style
        )
    )

    story.append(
        Paragraph(
            request.user.get_full_name() or request.user.username,
            name_style
        )
    )

    story.append(
        Paragraph(
            "For Successfully Completing",
            normal_style
        )
    )

    story.append(
        Paragraph(
            f"<b>{course.title}</b>",
            heading_style
        )
    )
    certificate, created = Certificate.objects.get_or_create(student=request.user,course=course)


    certificate_id = certificate.certificate_id
    verification_url = (
        request.build_absolute_uri(
            f"/courses/verify/{certificate_id}/"
        )
    )

    qr = qrcode.make(verification_url)

    qr_buffer = BytesIO()

    qr.save(qr_buffer, format="PNG")

    qr_buffer.seek(0)

    story.append(
        Paragraph(
            f"Completion Date : {certificate.issued_at.strftime('%d %B %Y')}",
            normal_style
        )
    )


    story.append(
        Paragraph(
            f"Certificate ID : <b>{certificate_id}</b>",
            normal_style
        )
    )

    story.append(
        Paragraph(
            "<br/><br/><br/>____________________________",
            normal_style
        )
    )

    story.append(
        Paragraph(
            "<b>Authorized Signature</b>",
            normal_style
        )
    )

    story.append(
        Paragraph(
            "AI LearnMate Certification Team",
            normal_style
        )
    )

    qr_image = Image(
        qr_buffer,
        width=120,
        height=120
    )

    qr_image.hAlign = "CENTER"

    story.append(qr_image)

    story.append(
        Paragraph(
            "Scan QR Code to Verify Certificate",
            normal_style
        )
    )
    document.build(
        story,
        onFirstPage=draw_certificate_border
    )

    return response



def verify_certificate(request, certificate_id):

    certificate = get_object_or_404(Certificate,certificate_id=certificate_id)

    return render(
        request,
        "courses/verify_certificate.html",
        {
            "certificate": certificate
        }
    )

def draw_certificate_border(canvas, doc):

    width, height = landscape(A4)

    canvas.saveState()

    canvas.setStrokeColor(HexColor("#C8A951"))
    canvas.setLineWidth(6)

    canvas.rect(
        20,
        20,
        width - 40,
        height - 40
    )

    canvas.setLineWidth(2)

    canvas.rect(
        35,
        35,
        width - 70,
        height - 70
    )

    canvas.restoreState()