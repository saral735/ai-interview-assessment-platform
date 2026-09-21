
from sqlalchemy import text

from app.core.database import engine


with engine.begin() as conn:

    conn.execute(
        text("""
            ALTER TABLE jobs
            ADD COLUMN created_by INTEGER REFERENCES users(id)
        """)
    )

    conn.execute(
        text("""
            UPDATE jobs
            SET created_by = (
                SELECT id
                FROM users
                WHERE role = 'recruiter'
                ORDER BY id
                LIMIT 1
            )
            WHERE created_by IS NULL
        """)
    )

    conn.execute(
        text("""
            ALTER TABLE jobs
            ALTER COLUMN created_by SET NOT NULL
        """)
    )


print("JOB OWNERSHIP COLUMN ADDED SUCCESSFULLY")
