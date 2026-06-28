from progress_tracker.models import ProgressTracker
from .models import StudyPlan


class StudyPlannerService:

    def generate_plan(self, student):

        StudyPlan.objects.filter(student=student).delete()

        progress = ProgressTracker.objects.get(student=student)

        if progress.progress_percentage < 50:

            topics = [
                ("Python Basics", "Revise variables, loops and functions."),
                ("Django ORM", "Practice models and queries."),
                ("SQL Basics", "Practice SELECT, INSERT and UPDATE.")
            ]

        elif progress.progress_percentage < 75:

            topics = [
                ("Django REST Framework", "Build serializers and APIs."),
                ("Authentication", "Practice Token Authentication."),
                ("Python OOP", "Revise inheritance and polymorphism.")
            ]

        else:

            topics = [
                ("System Design", "Study scalable architectures."),
                ("AI Integration", "Practice Gemini APIs."),
                ("Advanced Django", "Signals, caching and optimization.")
            ]

        for day, topic in enumerate(topics, start=1):

            StudyPlan.objects.create(
                student=student,
                title=topic[0],
                description=topic[1],
                day_number=day,
                estimated_minutes=60
            )

        return StudyPlan.objects.filter(student=student)