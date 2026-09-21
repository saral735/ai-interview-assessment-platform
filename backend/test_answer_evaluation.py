from app.services.answer_evaluation import evaluate_answer


question = """
Explain the difference between a list and a tuple in Python
and give examples of when you would use each.
"""

answer = """
A list is mutable, so we can add, remove or modify elements.
A tuple is immutable, so once created its elements cannot be changed.
I would use a list when data needs to change and a tuple
when the data should remain fixed.
"""


evaluation = evaluate_answer(
    question=question,
    answer=answer
)


print("\nAI EVALUATION:\n")

print("Technical Score:", evaluation["technical_score"])
print("Problem Solving Score:", evaluation["problem_solving_score"])
print("Communication Score:", evaluation["communication_score"])
print("Overall Score:", evaluation["overall_score"])
print("Feedback:", evaluation["feedback"])