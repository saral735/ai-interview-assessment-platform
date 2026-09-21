import json

from app.services.groq_service import generate_text


def generate_interview_questions(
    resume_context: str,
    job_context: str,
    blueprint: dict
) -> list[dict]:
    """
    Generate interview questions using the candidate resume,
    job description, and interview blueprint.
    """

    prompt = f"""
You are an AI technical interviewer.

Generate interview questions for a candidate based on
their resume and the job description.

CANDIDATE RESUME:
{resume_context}

JOB DESCRIPTION:
{job_context}

INTERVIEW BLUEPRINT:
{json.dumps(blueprint)}

Generate exactly the number of questions specified
in the blueprint.

Question categories:
- technical
- problem_solving
- projects
- behavioral

For every question return:
- question_text
- question_type
- difficulty
- question_order

Difficulty must be one of:
easy, medium, hard

Return ONLY valid JSON in this format:

[
    {{
        "question_text": "Question here",
        "question_type": "technical",
        "difficulty": "medium",
        "question_order": 1
    }}
]
"""

    response = generate_text(
        prompt=prompt,
        system_prompt=(
            "You are a professional AI interviewer. "
            "Generate relevant, clear and non-repetitive "
            "interview questions."
        )
    )

    try:
        questions = json.loads(response)
    except json.JSONDecodeError as exc:
        raise ValueError(
            "Groq returned invalid JSON"
        ) from exc

    if not isinstance(questions, list):
        raise ValueError(
            "Generated questions must be a list"
        )

    return questions