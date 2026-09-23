import os

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai


# Load environment variables
load_dotenv()


# Create Flask application
app = Flask(__name__)


# Get Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not configured.")


# Create Gemini client
client = genai.Client(api_key=api_key)


# --------------------------------------------------
# STRUCTURED PROMPT BUILDER
# --------------------------------------------------

def build_prompt(task, content):

    if task == "summarise":

        return f"""
You are an AI study assistant helping a student.

TASK:
Summarise the student's study notes.

INSTRUCTIONS:
- Write a concise summary.
- Identify the 5 most important points.
- Use simple, beginner-friendly language.
- Preserve the meaning of the original notes.
- Do not add information that is not supported by the notes.

OUTPUT FORMAT:

SUMMARY:
[Write a concise summary]

KEY POINTS:
1. [Important point]
2. [Important point]
3. [Important point]
4. [Important point]
5. [Important point]

STUDENT NOTES:
{content}
"""


    elif task == "quiz":

        return f"""
You are an AI tutor helping a student revise.

TASK:
Create a short quiz from the study material.

INSTRUCTIONS:
- Generate exactly 5 multiple-choice questions.
- Give 4 options for every question.
- Only one option should be correct.
- Base every question on the supplied study material.
- Include the correct answer.
- Include a short explanation for each answer.
- Use clear language appropriate for a student.

OUTPUT FORMAT:

QUESTION 1:
[Question]

A. [Option]
B. [Option]
C. [Option]
D. [Option]

ANSWER:
[Correct option]

EXPLANATION:
[Short explanation]

Repeat the same format for Questions 2, 3, 4 and 5.

STUDY MATERIAL:
{content}
"""


    elif task == "explain":

        return f"""
You are a friendly AI tutor.

TASK:
Explain the following topic to a beginner student.

INSTRUCTIONS:
- Give a simple definition.
- Explain the concept step by step.
- Give one practical example.
- Give a simple analogy where useful.
- Avoid unnecessarily complicated terminology.
- Make the explanation easy for a beginner to understand.

OUTPUT FORMAT:

DEFINITION:
[Simple definition]

HOW IT WORKS:
[Step-by-step explanation]

EXAMPLE:
[Practical example]

SIMPLE ANALOGY:
[Easy analogy]

TOPIC:
{content}
"""


    elif task == "improve":

        return f"""
You are an AI tutor helping a student improve their written answer.

TASK:
Review the student's answer and improve it while preserving
the original meaning.

INSTRUCTIONS:
- Correct grammar and spelling.
- Improve clarity and structure.
- Make the answer more complete where appropriate.
- Use appropriate academic language.
- Do not completely change the student's intended answer.
- Do not invent facts.
- Explain what could be improved.

OUTPUT FORMAT:

IMPROVED ANSWER:
[Write the improved version]

WHAT WAS IMPROVED:
- [Improvement 1]
- [Improvement 2]
- [Improvement 3]

SUGGESTION:
[One useful suggestion for the student]

STUDENT ANSWER:
{content}
"""


    return None


# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------

@app.route("/")
def home():

    return render_template("index.html")


# --------------------------------------------------
# AI GENERATION
# --------------------------------------------------

@app.route("/generate", methods=["POST"])
def generate():

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "error": "Invalid request."
            }), 400


        task = data.get("task", "").strip()

        content = data.get("content", "").strip()


        # ------------------------------
        # INPUT VALIDATION
        # ------------------------------

        if not content:

            return jsonify({
                "error": "Please enter some content first."
            }), 400


        if len(content) < 10:

            return jsonify({
                "error": "Please enter at least 10 characters."
            }), 400


        valid_tasks = [
            "summarise",
            "quiz",
            "explain",
            "improve"
        ]


        if task not in valid_tasks:

            return jsonify({
                "error": "Please select a valid study tool."
            }), 400


        # ------------------------------
        # BUILD STRUCTURED PROMPT
        # ------------------------------

        prompt = build_prompt(
            task,
            content
        )


        if not prompt:

            return jsonify({
                "error": "Unable to create the AI prompt."
            }), 400


        # ------------------------------
        # CALL GEMINI API
        # ------------------------------

        response = client.models.generate_content(

            model="gemini-3.5-flash-lite",

            contents=prompt

        )


        # ------------------------------
        # GET AI RESPONSE
        # ------------------------------

        result = response.text


        if not result or not result.strip():

            return jsonify({
                "error": "The AI returned an empty response."
            }), 500


        # ------------------------------
        # SEND RESPONSE TO FRONTEND
        # ------------------------------

        return jsonify({
            "result": result
        })


    except Exception as e:

        print("Error:", e)

        return jsonify({
            "error":
                "The AI service could not process your request. "
                "Please check your API key and available API access."
        }), 500


# --------------------------------------------------
# START APPLICATION
# --------------------------------------------------

if __name__ == "__main__":

    app.run(
        debug=True
    )
