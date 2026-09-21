
import json

from app.services.groq_service import generate_text


def evaluate_answer(
    question: str,
    answer: str
) -> dict:
    """
    Evaluate a candidate answer using an LLM.
    """

    prompt = f"""
You are an expert professional interviewer.

Evaluate the candidate's answer based on the question.

QUESTION:
{question}

CANDIDATE ANSWER:
{answer}

Evaluate the candidate on these five categories:

1. Technical Knowledge
2. Problem Solving
3. Project Understanding
4. Communication
5. Behavioral / Professional Approach

Give each score from 0 to 100.

Evaluation rules:
- Score only based on the candidate's answer.
- Do not assume skills that are not demonstrated.
- Give lower scores when the answer is incomplete or incorrect.
- Give higher scores when the answer is accurate, relevant and well explained.
- Keep the evaluation objective and consistent.

Also provide short constructive feedback.

Return ONLY valid JSON.
Do not use markdown.
Do not use ```json.
Do not add any text before or after the JSON.

Return exactly this format:

{{
    "technical_score": 0,
    "problem_solving_score": 0,
    "project_score": 0,
    "communication_score": 0,
    "behavioral_score": 0,
    "feedback": "Short constructive feedback"
}}
"""

    response = generate_text(
        prompt=prompt,
        system_prompt=(
            "You are an objective and professional AI interviewer. "
            "Evaluate candidate answers fairly, consistently and "
            "strictly based on the evidence provided in the answer. "
            "Always return valid JSON only."
        )
    )

    try:
        response = response.strip()

        # Remove markdown code fences if the LLM adds them
        if response.startswith("```"):
            response = response.replace("```json", "")
            response = response.replace("```", "")
            response = response.strip()

        evaluation = json.loads(response)

    except json.JSONDecodeError as exc:
        print("\nRAW GROQ RESPONSE:\n")
        print(response)

        raise ValueError(
            "Groq returned invalid evaluation JSON"
        ) from exc

    required_fields = [
        "technical_score",
        "problem_solving_score",
        "project_score",
        "communication_score",
        "behavioral_score",
        "feedback"
    ]

    for field in required_fields:
        if field not in evaluation:
            raise ValueError(
                f"Missing evaluation field: {field}"
            )

    # Validate score values
    score_fields = [
        "technical_score",
        "problem_solving_score",
        "project_score",
        "communication_score",
        "behavioral_score"
    ]

    for field in score_fields:
        score = evaluation[field]

        if not isinstance(score, (int, float)):
            raise ValueError(
                f"{field} must be a number"
            )

        if not 0 <= score <= 100:
            raise ValueError(
                f"{field} must be between 0 and 100"
            )

    return evaluation
