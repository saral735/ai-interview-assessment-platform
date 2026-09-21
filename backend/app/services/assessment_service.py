def determine_assessment_result(
    final_score: float,
    passing_score: float,
    confidence: float
) -> str:
    """
    Determine the final candidate assessment result.
    """

    if confidence < 60:
        return "REVIEW"

    if final_score >= passing_score:
        return "PASS"

    if final_score < passing_score - 10:
        return "FAIL"

    return "REVIEW"