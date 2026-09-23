# 🎓 AI Study Buddy

AI Study Buddy is an AI-powered student utility application built with Flask and the Gemini API.

It helps students with four common study tasks:

- 📝 Summarise Notes
- ❓ Generate Quiz
- 💡 Explain Concepts
- ✍️ Improve Answers

## Features

- Simple student-friendly interface
- Structured prompts for each AI task
- Gemini API integration
- Input validation
- Error handling
- Readable AI-generated responses

## Technologies Used

- Python
- Flask
- Google Gemini API
- HTML
- CSS
- JavaScript

## How It Works

1. Student enters notes, a topic, or an answer.
2. Student selects an AI study feature.
3. JavaScript validates the input.
4. Flask receives the request.
5. A structured prompt is created.
6. The prompt is sent to the Gemini API.
7. The generated response is returned to the browser.

## Setup

Create a virtual environment:

```bash
python -m venv venv