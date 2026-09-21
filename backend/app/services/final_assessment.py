from app.services.assessment_service import determine_assessment_result


def calculate_final_interview_assessment(
    evaluations: list[dict],
    passing_score: float
) -> dict:
    """
    Calculate the final interview assessment
    from all answer evaluations.
    """

    if not evaluations:
        raise ValueError(
            "No evaluations found for this interview"
        )

    total_score = sum(
        evaluation["overall_score"]
        for evaluation in evaluations
    )

    final_score = round(
        total_score / len(evaluations),
        2
    )

    # Calculate confidence based on available evaluations.
    # More evaluated answers provide higher confidence.
    confidence = min(
        100.0,
        round((len(evaluations) / 9) * 100, 2)
    )

    result = determine_assessment_result(
        final_score=final_score,
        passing_score=passing_score,
        confidence=confidence
    )

    return {
        "final_score": final_score,
        "confidence": confidence,
        "result": result,
        "evaluated_answers": len(evaluations)
    }