def calculate_final_score(
    technical_score: float,
    problem_solving_score: float,
    project_score: float,
    communication_score: float,
    behavioral_score: float
) -> float:
    """
    Calculate final interview score using backend-controlled weights.
    """

    final_score = (
        technical_score * 0.40
        + problem_solving_score * 0.20
        + project_score * 0.15
        + communication_score * 0.10
        + behavioral_score * 0.15
    )

    return round(final_score, 2)