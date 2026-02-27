from pydantic import BaseModel, EmailStr, validator
from typing import Optional,List
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    roles: List[str] = []

    @validator("roles", pre=True, check_fields=False)
    def get_role_names(cls, v):
        if v and isinstance(v[0], object) and hasattr(v[0], "name"):
            return [r.name for r in v]
        return []

    class Config:
        from_attributes = True