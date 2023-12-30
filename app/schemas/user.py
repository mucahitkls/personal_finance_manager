from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserLogin(UserCreate):
    pass


class UserInDB(UserBase):
    hashed_password: str
