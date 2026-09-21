import re


def normalize_skill(skill: str) -> str:
    """
    Convert a skill into a consistent format
    for reliable matching.
    """

    skill = skill.strip().lower()

    skill = re.sub(
        r"\s+",
        " ",
        skill
    )

    return skill


def parse_skills(skills_text: str | None) -> list[str]:
    """
    Convert comma-separated skills into
    normalized skill list.
    """

    if not skills_text:
        return []

    skills = skills_text.split(",")

    return [
        normalize_skill(skill)
        for skill in skills
        if skill.strip()
    ]

KNOWN_SKILLS = {
    "python",
    "java",
    "c",
    "c++",
    "sql",
    "mysql",
    "postgresql",
    "fastapi",
    "django",
    "spring boot",
    "hibernate",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "numpy",
    "pandas",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "llm",
    "rag",
    "qdrant",
    "langchain",
    "git",
    "docker",
    "javascript",
    "react",
    "html",
    "css"
}


def extract_resume_skills(
    resume_text: str
) -> list[str]:

    normalized_text = resume_text.lower()

    found_skills = []

    for skill in KNOWN_SKILLS:

        if skill in normalized_text:
            found_skills.append(skill)

    return sorted(found_skills)

def calculate_skill_match(
    required_skills: str | None,
    preferred_skills: str | None,
    resume_text: str
) -> dict:

    required = set(
        parse_skills(required_skills)
    )

    preferred = set(
        parse_skills(preferred_skills)
    )

    resume_skills = set(
        extract_resume_skills(resume_text)
    )

    matched_required = sorted(
        required.intersection(resume_skills)
    )

    missing_required = sorted(
        required.difference(resume_skills)
    )

    matched_preferred = sorted(
        preferred.intersection(resume_skills)
    )

    missing_preferred = sorted(
        preferred.difference(resume_skills)
    )

    if required:
        required_match_percentage = (
            len(matched_required)
            / len(required)
        ) * 100
    else:
        required_match_percentage = 100.0

    if preferred:
        preferred_match_percentage = (
            len(matched_preferred)
            / len(preferred)
        ) * 100
    else:
        preferred_match_percentage = 100.0

    overall_match_percentage = (
        required_match_percentage * 0.7
        + preferred_match_percentage * 0.3
    )

    return {
        "matched_required": matched_required,
        "missing_required": missing_required,
        "matched_preferred": matched_preferred,
        "missing_preferred": missing_preferred,
        "required_match_percentage": round(
            required_match_percentage,
            2
        ),
        "preferred_match_percentage": round(
            preferred_match_percentage,
            2
        ),
        "overall_match_percentage": round(
            overall_match_percentage,
            2
        )
    }