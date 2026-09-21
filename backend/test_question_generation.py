from app.services.question_generation import generate_interview_questions
from app.services.interview_blueprint import get_interview_blueprint


resume_context = """
Candidate has experience with Python, Java, SQL, FastAPI,
RAG, LangChain, PostgreSQL and Qdrant.
The candidate has worked on AI and backend development projects.
"""

job_context = """
We are looking for a Python AI/ML Engineer.
The candidate should have knowledge of Python,
Machine Learning, RAG, FastAPI, LLMs and vector databases.
"""

blueprint = get_interview_blueprint()


questions = generate_interview_questions(
    resume_context=resume_context,
    job_context=job_context,
    blueprint=blueprint
)


print("\nGENERATED QUESTIONS:\n")

for question in questions:
    print(
        f"{question['question_order']}. "
        f"[{question['question_type']}] "
        f"[{question['difficulty']}] "
        f"{question['question_text']}"
    )

print("\nTOTAL QUESTIONS:", len(questions))