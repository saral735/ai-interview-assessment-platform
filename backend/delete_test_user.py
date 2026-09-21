from sqlalchemy import text
from app.core.database import engine

with engine.connect() as conn:
    conn.execute(
        text("DELETE FROM users WHERE email = :email"),
        {"email": "testuser@example.com"}
    )
    conn.commit()

print("USER DELETED")