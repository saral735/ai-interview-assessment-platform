
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models.answer import Answer
from app.models.evaluation import Evaluation
from app.core.database import get_db
from app.models.interview import Interview
from app.models.candidate import Candidate
from app.models.job import Job
from app.models.question import Question

from app.schemas.interview import InterviewCreate, InterviewResponse

from app.services.interview_blueprint import get_interview_blueprint
from app.services.question_generation import generate_interview_questions
from app.services.answer_evaluation import evaluate_answer
from app.services.scoring_service import calculate_final_score
from app.services.final_assessment import calculate_final_interview_assessment


router = APIRouter(
    prefix="/interviews",
    tags=["Interviews"]
)


@router.post(
    "/",
    response_model=InterviewResponse,
    status_code=status.HTTP_201_CREATED
)
def create_interview(
    interview_data: InterviewCreate,
    db: Session = Depends(get_db)
):
    # Find candidate
    candidate = db.query(Candidate).filter(
        Candidate.id == interview_data.candidate_id
    ).first()

    if not candidate:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found"
        )

    # Find job
    job = db.query(Job).filter(
        Job.id == interview_data.job_id
    ).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    # Create interview
    interview = Interview(
        candidate_id=interview_data.candidate_id,
        job_id=interview_data.job_id,
        status="CREATED"
    )

    db.add(interview)
    db.commit()
    db.refresh(interview)

    try:
        # Get interview blueprint
        blueprint = get_interview_blueprint()

        # Resume context
        resume_context = candidate.resume_text or ""

        # Job context
        job_context = job.description or ""

        # Generate AI questions
        generated_questions = generate_interview_questions(
            resume_context=resume_context,
            job_context=job_context,
            blueprint=blueprint
        )

        # Save questions in database
        for question_data in generated_questions:
            question = Question(
                interview_id=interview.id,
                question_text=question_data["question_text"],
                question_type=question_data["question_type"],
                difficulty=question_data["difficulty"],
                question_order=question_data["question_order"],
                is_answered=0
            )

            db.add(question)

        # Update interview status
        interview.status = "READY"

        db.commit()
        db.refresh(interview)

    except Exception as exc:
        db.rollback()

        # Remove partially created interview
        db.query(Interview).filter(
            Interview.id == interview.id
        ).delete()

        db.commit()

        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate interview questions: {str(exc)}"
        )

    return interview


@router.get(
    "/{interview_id}/questions"
)
def get_interview_questions(
    interview_id: int,
    db: Session = Depends(get_db)
):
    interview = db.query(Interview).filter(
        Interview.id == interview_id
    ).first()

    if not interview:
        raise HTTPException(
            status_code=404,
            detail="Interview not found"
        )

    questions = db.query(Question).filter(
        Question.interview_id == interview_id
    ).order_by(
        Question.question_order.asc()
    ).all()

    return {
        "interview_id": interview_id,
        "total_questions": len(questions),
        "questions": questions
    }


@router.get(
    "/{interview_id}/next-question"
)
def get_next_question(
    interview_id: int,
    db: Session = Depends(get_db)
):
    interview = db.query(Interview).filter(
        Interview.id == interview_id
    ).first()

    if not interview:
        raise HTTPException(
            status_code=404,
            detail="Interview not found"
        )

    next_question = db.query(Question).filter(
        Question.interview_id == interview_id,
        Question.is_answered == 0
    ).order_by(
        Question.question_order.asc()
    ).first()

    if not next_question:
        return {
            "interview_id": interview_id,
            "message": "Interview completed",
            "question": None
        }

    return {
        "interview_id": interview_id,
        "question": next_question
    }


@router.post(
    "/{interview_id}/questions/{question_id}/answer"
)
def submit_answer(
    interview_id: int,
    question_id: int,
    answer_text: str,
    db: Session = Depends(get_db)
):
    # Check interview
    interview = db.query(Interview).filter(
        Interview.id == interview_id
    ).first()

    if not interview:
        raise HTTPException(
            status_code=404,
            detail="Interview not found"
        )

    # Check question
    question = db.query(Question).filter(
        Question.id == question_id,
        Question.interview_id == interview_id
    ).first()

    if not question:
        raise HTTPException(
            status_code=404,
            detail="Question not found"
        )

    # Prevent duplicate answer
    existing_answer = db.query(Answer).filter(
        Answer.question_id == question_id
    ).first()

    if existing_answer:
        raise HTTPException(
            status_code=400,
            detail="Answer already submitted for this question"
        )

    # Validate answer
    if not answer_text.strip():
        raise HTTPException(
            status_code=400,
            detail="Answer cannot be empty"
        )

    # Save answer
    answer = Answer(
        question_id=question_id,
        answer_text=answer_text.strip()
    )

    db.add(answer)
    db.flush()

    try:
        # AI evaluates the candidate answer
        ai_evaluation = evaluate_answer(
            question=question.question_text,
            answer=answer.answer_text
        )

        # Backend calculates the weighted score
        final_score = calculate_final_score(
            technical_score=ai_evaluation["technical_score"],
            problem_solving_score=ai_evaluation["problem_solving_score"],
            project_score=ai_evaluation["project_score"],
            communication_score=ai_evaluation["communication_score"],
            behavioral_score=ai_evaluation["behavioral_score"]
        )

        # Save evaluation
        evaluation = Evaluation(
            answer_id=answer.id,
            technical_score=ai_evaluation["technical_score"],
            problem_solving_score=ai_evaluation["problem_solving_score"],
            project_score=ai_evaluation["project_score"],
            communication_score=ai_evaluation["communication_score"],
            behavioral_score=ai_evaluation["behavioral_score"],
            overall_score=final_score,
            feedback=ai_evaluation["feedback"]
        )

        db.add(evaluation)

        # Mark question as answered
        question.is_answered = 1

        db.commit()

        db.refresh(answer)
        db.refresh(evaluation)

    except Exception as exc:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Failed to evaluate answer: {str(exc)}"
        )

    return {
        "message": "Answer submitted and evaluated successfully",
        "interview_id": interview_id,
        "question_id": question_id,
        "answer_id": answer.id,
        "evaluation_id": evaluation.id,
        "is_answered": question.is_answered,
        "evaluation": {
            "technical_score": evaluation.technical_score,
            "problem_solving_score": evaluation.problem_solving_score,
            "project_score": evaluation.project_score,
            "communication_score": evaluation.communication_score,
            "behavioral_score": evaluation.behavioral_score,
            "overall_score": evaluation.overall_score,
            "feedback": evaluation.feedback
        }
    }


@router.post(
    "/{interview_id}/complete"
)
def complete_interview(
    interview_id: int,
    db: Session = Depends(get_db)
):
    interview = db.query(Interview).filter(
        Interview.id == interview_id
    ).first()

    if not interview:
        raise HTTPException(
            status_code=404,
            detail="Interview not found"
        )

    unanswered_count = db.query(Question).filter(
        Question.interview_id == interview_id,
        Question.is_answered == 0
    ).count()

    if unanswered_count > 0:
        raise HTTPException(
            status_code=400,
            detail=f"{unanswered_count} questions are still unanswered"
        )

    interview.status = "COMPLETED"

    db.commit()
    db.refresh(interview)

    return {
        "message": "Interview completed successfully",
        "interview_id": interview.id,
        "status": interview.status
    }
@router.post(
    "/{interview_id}/assessment"
)
def generate_final_assessment(
    interview_id: int,
    db: Session = Depends(get_db)
):
    # Check interview
    interview = db.query(Interview).filter(
        Interview.id == interview_id
    ).first()

    if not interview:
        raise HTTPException(
            status_code=404,
            detail="Interview not found"
        )

    # Get job
    job = db.query(Job).filter(
        Job.id == interview.job_id
    ).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    # Get all questions
    questions = db.query(Question).filter(
        Question.interview_id == interview_id
    ).order_by(
        Question.question_order
    ).all()

    if not questions:
        raise HTTPException(
            status_code=400,
            detail="No questions found for this interview"
        )

    # Make sure all questions are answered
    unanswered_count = sum(
        1
        for question in questions
        if question.is_answered == 0
    )

    if unanswered_count > 0:
        raise HTTPException(
            status_code=400,
            detail=f"{unanswered_count} questions are still unanswered"
        )

    # Get evaluations for all answers
    evaluations = []

    for question in questions:

        answer = db.query(Answer).filter(
            Answer.question_id == question.id
        ).first()

        if not answer:
            raise HTTPException(
                status_code=400,
                detail=f"Answer not found for question {question.id}"
            )

        evaluation = db.query(Evaluation).filter(
            Evaluation.answer_id == answer.id
        ).first()

        if not evaluation:
            raise HTTPException(
                status_code=400,
                detail=f"Evaluation not found for question {question.id}"
            )

        evaluations.append({
            "overall_score": evaluation.overall_score
        })

    # Calculate final assessment
    assessment = calculate_final_interview_assessment(
        evaluations=evaluations,
        passing_score=job.passing_score
    )

    return {
        "message": "Final interview assessment generated successfully",
        "interview_id": interview.id,
        "candidate_id": interview.candidate_id,
        "job_id": interview.job_id,
        "total_questions": len(questions),
        "evaluated_answers": assessment["evaluated_answers"],
        "final_score": assessment["final_score"],
        "passing_score": job.passing_score,
        "confidence": assessment["confidence"],
        "result": assessment["result"]
    }