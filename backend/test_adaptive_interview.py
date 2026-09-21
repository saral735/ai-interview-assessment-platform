from app.services.adaptive_interview import determine_next_difficulty


tests = [
    ("easy", 90),
    ("medium", 85),
    ("hard", 90),
    ("hard", 40),
    ("medium", 40),
    ("easy", 40),
    ("medium", 65),
]


for current_difficulty, score in tests:

    next_difficulty = determine_next_difficulty(
        current_difficulty=current_difficulty,
        score=score
    )

    print(
        f"Current: {current_difficulty} | "
        f"Score: {score} | "
        f"Next: {next_difficulty}"
    )