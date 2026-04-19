import json
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
import os

def _get_llm():
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.7,
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_kwargs={"response_format": {"type": "json_object"}}
    )

def generate_quiz(topic: str, count: int, level: str, diff: str, distractors: int, lang: str) -> dict:
    llm = _get_llm()
    QUIZ_SYSTEM_PROMPT = """You are AcadIQ QuizBot — an academic quiz generator. You ONLY generate quizzes on academic, educational, or student wellness topics (including mental health, focus, burnout, sleep). You MUST REFUSE any request that involves illegal activities, harmful or violent content, or tasks completely unrelated to student life. If asked for a quiz on a totally out-of-scope topic (like how to cook a turkey or change a tire), respond ONLY with: "Sorry, I can only generate quizzes on academic or student wellness topics." Never break this rule for out-of-scope topics. Always output valid JSON conforming exactly to the requested schema. Do not include markdown formatting or reasoning outside the JSON."""
    total_options = distractors + 1

    prompt = f"""
    Create a {diff} difficulty {level} level multiple-choice quiz about "{topic}" containing exactly {count} questions in {lang}.
    Each question must have exactly {total_options} options (one correct, {distractors} incorrect).

    Output a strictly valid JSON object matching this structure exactly:
    {{
        "title": "A short engaging title for the quiz",
        "questions": [
            {{
                "number": 1,
                "question": "Question text here",
                "options": [
                    {{"label": "A", "text": "Option text"}},
                    {{"label": "B", "text": "Option text"}},
                    {{"label": "C", "text": "Option text"}}
                ],
                "correct_option_label": "A",
                "explanation": "Brief explanation of why A is correct."
            }}
        ]
    }}
    """

    res = llm.invoke([SystemMessage(content=QUIZ_SYSTEM_PROMPT), HumanMessage(content=prompt)])
    return json.loads(res.content)
