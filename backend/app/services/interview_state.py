from app.services.adaptive_interview import determine_next_difficulty


def get_next_question_state(
    current_difficulty: str,
    answer_score: float
) -> dict:
    """
    Determine the state for the candidate's next question.
    """

    next_difficulty = determine_next_difficulty(
        current_difficulty=current_difficulty,
        score=answer_score
    )

    return {
        "current_difficulty": current_difficulty,
        "answer_score": answer_score,
        "next_difficulty": next_difficulty
    }