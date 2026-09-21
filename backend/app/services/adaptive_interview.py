def determine_next_difficulty(
    current_difficulty: str,
    score: float
) -> str:
    """
    Determine the next question difficulty
    based on the candidate's previous answer score.
    """

    if score >= 80:
        if current_difficulty == "easy":
            return "medium"

        if current_difficulty == "medium":
            return "hard"

        return "hard"

    if score < 50:
        if current_difficulty == "hard":
            return "medium"

        if current_difficulty == "medium":
            return "easy"

        return "easy"

    return current_difficulty