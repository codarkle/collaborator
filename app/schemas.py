from pydantic import BaseModel, EmailStr
from typing import Optional

class EmailCreate(BaseModel):
    name: str
    email: EmailStr
    msg: Optional[str] = None

class EmailResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    msg: Optional[str]

    class Config:
        from_attributes = True
