from app.services.groq_service import generate_text


def generate_follow_up_question(
    previous_question: str,
    previous_answer: str,
    difficulty: str,
    job_context: str
) -> dict:
    """
    Generate an adaptive follow-up question based on
    the candidate's previous answer.
    """

    prompt = f"""
You are an adaptive AI interviewer.

Previous Question:
{previous_question}

Candidate Answer:
{previous_answer}

Current Difficulty:
{difficulty}

Job Context:
{job_context}

Generate ONE follow-up interview question.

Rules:
- The question must be relevant to the previous answer.
- Do not repeat the previous question.
- If the answer is strong, make the question more challenging.
- If the answer is weak, ask a simpler supporting question.
- Keep the question practical and interview-focused.

Return ONLY valid JSON:

{{
    "question_text": "Your question",
    "question_type": "technical",
    "difficulty": "medium"
}}
"""

    response = generate_text(
        prompt=prompt,
        system_prompt=(
            "You are a professional adaptive technical interviewer. "
            "Generate one clear and relevant follow-up question."
        )
    )

    import json

    try:
        question = json.loads(response)
    except json.JSONDecodeError as exc:
        raise ValueError(
            "Groq returned invalid JSON"
        ) from exc

    return question