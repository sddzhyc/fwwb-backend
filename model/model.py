from typing import List, Optional
from sqlalchemy import Join
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select

class User(SQLModel,table = True):
    id: Optional[int] = Field(default=None, primary_key=True)
    password: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    
    jobs: List["Job"] = Relationship(back_populates="user")

class Job(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str]
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: User = Relationship(back_populates="jobs")

class UserCreate(SQLModel):
    username: str
    password: str
    email : Optional[str] = None


class UserRead(SQLModel):
    id: int
    username: str
    email: str
    full_name: Optional[str] = None
    



