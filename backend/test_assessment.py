from app.services.assessment_service import determine_assessment_result


test_cases = [
    {
        "final_score": 85,
        "passing_score": 70,
        "confidence": 90
    },
    {
        "final_score": 50,
        "passing_score": 70,
        "confidence": 90
    },
    {
        "final_score": 65,
        "passing_score": 70,
        "confidence": 90
    },
    {
        "final_score": 80,
        "passing_score": 70,
        "confidence": 40
    }
]


print("\nASSESSMENT RESULTS:\n")


for case in test_cases:
    result = determine_assessment_result(
        final_score=case["final_score"],
        passing_score=case["passing_score"],
        confidence=case["confidence"]
    )

    print(
        f"Score: {case['final_score']}, "
        f"Passing: {case['passing_score']}, "
        f"Confidence: {case['confidence']} "
        f"-> {result}"
    )