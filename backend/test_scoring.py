from app.services.scoring_service import calculate_final_score


technical_score = 70
problem_solving_score = 75
project_score = 80
communication_score = 85
behavioral_score = 90


final_score = calculate_final_score(
    technical_score=technical_score,
    problem_solving_score=problem_solving_score,
    project_score=project_score,
    communication_score=communication_score,
    behavioral_score=behavioral_score
)


print("\nBACKEND SCORING:\n")

print("Technical Score:", technical_score)
print("Problem Solving Score:", problem_solving_score)
print("Project Score:", project_score)
print("Communication Score:", communication_score)
print("Behavioral Score:", behavioral_score)

print("Final Score:", final_score)