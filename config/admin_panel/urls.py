from django.urls import path
from . import views

urlpatterns = [

    path("",views.admin_dashboard,name="admin_dashboard"),

    path("students/",views.students,name="admin_students"),

    path("students/<int:user_id>/",views.student_detail,name="student_detail"),

    path("students/<int:user_id>/edit/",views.edit_student,name="edit_student"),


    path("students/<int:user_id>/delete/",views.delete_student,name="delete_student"),

    path("courses/",views.courses,name="admin_courses"),

    path("courses/add/",views.add_course,name="admin_add_course"),

    path("courses/<int:course_id>/edit/",views.edit_course,name="admin_edit_course",),

    path("courses/<int:course_id>/delete/",views.delete_course,name="admin_delete_course",),

    path("materials/",views.materials,name="admin_materials",),

    path("materials/add/",views.add_material,name="admin_add_material",),

    path("materials/edit/<int:pk>/",views.edit_material,name="admin_edit_material",),

    path("materials/delete/<int:pk>/",views.delete_material,name="admin_delete_material",),

    path("quizzes/",views.admin_quizzes,name="admin_quizzes",),

    path("quizzes/add/",views.add_quiz,name="admin_add_quiz",),

    path("quizzes/<int:quiz_id>/edit/",views.edit_quiz,name="admin_edit_quiz",),

    path("quizzes/<int:quiz_id>/delete/",views.delete_quiz,name="admin_delete_quiz",),

    path("quizzes/<int:quiz_id>/questions/",views.admin_questions,name="admin_questions",),

    path("quizzes/<int:quiz_id>/questions/add/",views.add_question,name="admin_add_question",),

    path("questions/<int:question_id>/edit/",views.edit_question,name="admin_edit_question",),

    path("questions/<int:question_id>/delete/",views.delete_question,name="admin_delete_question",),

    path("results/",views.student_results,name="admin_student_results",),

    path("progress/",views.progress_management,name="admin_progress",),

    path("ai-chat/",views.ai_chat_sessions,name="admin_ai_chat",),

    path("ai-chat/<int:session_id>/",views.chat_detail,name="admin_chat_detail",),

    path("ai-chat/delete/<int:session_id>/",views.delete_chat_session,name="admin_delete_chat",),

    path("certificates/",views.certificates,name="admin_certificates",),

    path("notifications/",views.notifications,name="admin_notifications",),

    path("notifications/add/",views.add_notification,name="admin_add_notification",),

    path("notifications/<int:notification_id>/edit/",views.edit_notification,name="admin_edit_notification",),

    path("notifications/<int:notification_id>/delete/",views.delete_notification,name="admin_delete_notification",),


]