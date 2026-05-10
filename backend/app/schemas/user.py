from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    full_name: str | None = None


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserRead(UserBase):
    id: int
    is_admin: bool

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
