import google.generativeai as genai
from django.conf import settings
#
# client = OpenAI(
#     api_key=settings.OPENAI_API_KEY
# )
# ============================================
# Gemini AI Tutor Service
# Uses Google Gemini API to answer student
# questions based on learning content
# ============================================

# Generate AI response using Gemini API
class AIService:

    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def ask_ai(self, prompt):

        response = self.model.generate_content(
            f"""
            You are an AI Tutor for AI LearnMate.

            Explain concepts clearly.
            Use simple English.
            Give examples whenever possible.

            Student Question:
            {prompt}
            """
        )

        return response.text