from app.services.adaptive_question import generate_follow_up_question


question = generate_follow_up_question(
    previous_question=(
        "Explain the difference between a list and a tuple in Python."
    ),
    previous_answer=(
        "A list is mutable, while a tuple is immutable. "
        "Lists are useful when data needs to change."
    ),
    difficulty="easy",
    job_context=(
        "Python AI/ML Engineer with Python, Machine Learning, "
        "RAG and FastAPI requirements."
    )
)


print("\nADAPTIVE FOLLOW-UP QUESTION:\n")
print(question)