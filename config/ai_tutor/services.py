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
# class AIService:
#
#     def __init__(self):
#         genai.configure(api_key=settings.GEMINI_API_KEY)
#         self.model = genai.GenerativeModel("gemini-2.5-flash")
#         print("Gemini Key:", settings.GEMINI_API_KEY)
#
#
# def ask_ai(self, prompt):
#     try:
#
#         response = self.model.generate_content(
#             f"""
#              You are an AI Tutor for AI LearnMate.
#
#              Explain concepts clearly.
#              Use simple English.
#              Give examples whenever possible.
#
#              Student Question:
#              {prompt}
#              """
#         )
#
#         return response.text
#
#     except Exception as e:
#
#         error = str(e)
#
#         if "quota" in error.lower():
#             return (
#                 "⚠️ Gemini API daily limit reached.\n\n"
#                 "Please try again later or use another API key."
#             )
#
#         return f"AI Error: {error}"

import google.generativeai as genai
from django.conf import settings


# ============================================
# Gemini AI Tutor Service
# ============================================

class AIService:

    def __init__(self):

        genai.configure(api_key=settings.GEMINI_API_KEY)

        self.model = genai.GenerativeModel("gemini-2.5-flash")

        print("Gemini Key:", settings.GEMINI_API_KEY)


    def ask_ai(self, prompt):

        try:

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

            if response and hasattr(response, "text"):

                return response.text

            return "No response generated."

        except Exception as e:

            error = str(e)

            if "quota" in error.lower():

                return (
                    "⚠️ Gemini API daily limit reached.\n\n"
                    "Please try again later or use another API key."
                )

            return f"AI Error: {error}"