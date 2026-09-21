from app.services.interview_state import get_next_question_state


tests = [
    ("easy", 90),
    ("medium", 85),
    ("hard", 40),
    ("medium", 65),
]


for difficulty, score in tests:

    state = get_next_question_state(
        current_difficulty=difficulty,
        answer_score=score
    )

    print(
        f"Current: {state['current_difficulty']} | "
        f"Score: {state['answer_score']} | "
        f"Next: {state['next_difficulty']}"
    )