from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: str = "candidate"


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int

    model_config = {
        "from_attributes": True
    }