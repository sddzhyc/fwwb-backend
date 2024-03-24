from typing import List, Optional
from sqlalchemy import Join
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select

from app.model import company


class CompanyBase(SQLModel):
    name: str
    description: Optional[str] =None

#TODO:添加完善Company类：修改Relationship关系
class Company(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str]
    users:List["User"] = Relationship(back_populates="company")
    # jobs: List["Job"] = Relationship(back_populates="company") #job和company无外键关联就不能加这个字段

class User(SQLModel,table = True):
    id: Optional[int] = Field(default=None, primary_key=True)
    password: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    company_id: Optional[int] = Field(default=None, foreign_key="company.id")
    company : Company = Relationship(back_populates="users")
    jobs: List["Job"] = Relationship(back_populates="user")

#TODO:重构Job类，提取字段到JobBase类
class Job(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str]
    maxSalary: int
    minSalary: int
    education: int
    tags: Optional[str] = None #json格式的数组序列化后存储
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: User = Relationship(back_populates="jobs")

class UserCreate(SQLModel):
    username: str
    password: str
    email : Optional[str] = None
    company_id: Optional[int] = None


class UserRead(SQLModel):
    id: int
    username: str
    email: str
    full_name: Optional[str] = None


# 定义ReadCompany、CreateCompany、UpdateCompany、DeleteCompany类
class CompanyRead(CompanyBase):
    id: int


class UserReadWithCompany(UserRead):
    company: Optional[CompanyRead] = None
    



