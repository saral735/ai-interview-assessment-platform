
from fastapi import Depends, HTTPException, status

from app.core.security import security, verify_access_token


def require_role(required_role: str):

    def role_checker(
        credentials=Depends(security)
    ):
        token = credentials.credentials

        payload = verify_access_token(token)

        user_role = payload.get("role")

        if user_role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource"
            )

        return payload

    return role_checker
