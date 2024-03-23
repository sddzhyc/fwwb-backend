
from typing import List, Optional
from fastapi import HTTPException
from requests import session
from rsa import verify
# from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select
from typing import Union
from app.model.model import User, UserCreate, UserRead
from app.utils.db import getSession
from app.model.job import JobRead

# sqlite_file_name = "database.db"
# sqlite_url = f"sqlite:///{sqlite_file_name}"
# connect_args = {"check_same_thread": False}
# engine = create_engine(mySQL_url, echo=True, connect_args=connect_args)
class UserReadWithjobs(UserRead):
    jobs: List[JobRead] = []

class UserService:
    def __init__(self, session: Session):
        self.session = session

    def getUser(self, username: str) -> User | None:
        # with getSession() as session: 
        session2 = getSession()
        user = session2.exec(select(User).where(User.username == username)).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

# 通过用户名获取用户，但是不返回密码，可用于验证用户是否登录
def vertifyUser(username: str):
    with getSession() as session:
    # session = getSession()
        user = session.exec(select(User).where(User.username == username)).first()
        user = UserRead.model_validate(user)
    return user

def initUser():
    user1 = User(username='johndoe',password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
                 email="johndoe@example.com", disabled=False)
    with getSession() as session:
        session.add(user1)
        session.commit()

def updateUser(user: User):
    with getSession() as session:
        session.add(user)
        session.commit()

def createUser(userCreate: UserCreate):
    with getSession() as session:
        # db_user = User.model_validate(user, update={"company_id": companyId}) 
        db_user = User.model_validate(userCreate )
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user

def deleteUser():
    pass
# if __name__ == "__main__":
#     main()d