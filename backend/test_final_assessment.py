from app.services.final_assessment import (
    calculate_final_interview_assessment
)


evaluations = [
    {"overall_score": 70},
    {"overall_score": 80},
    {"overall_score": 75},
    {"overall_score": 85},
    {"overall_score": 90},
    {"overall_score": 72},
    {"overall_score": 78},
    {"overall_score": 88},
    {"overall_score": 82},
]


result = calculate_final_interview_assessment(
    evaluations=evaluations,
    passing_score=70
)


print("\nFINAL INTERVIEW ASSESSMENT:\n")

print("Final Score:", result["final_score"])
print("Confidence:", result["confidence"])
print("Result:", result["result"])
print("Evaluated Answers:", result["evaluated_answers"])