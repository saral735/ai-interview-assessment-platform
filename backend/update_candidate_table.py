
from sqlalchemy import text

from app.core.database import engine


with engine.begin() as conn:

    conn.execute(
        text("""
            CREATE INDEX IF NOT EXISTS ix_candidates_email
            ON candidates (email)
        """)
    )

    conn.execute(
        text("""
            CREATE INDEX IF NOT EXISTS ix_candidates_user_id
            ON candidates (user_id)
        """)
    )


print("CANDIDATE TABLE UPDATED SUCCESSFULLY")
