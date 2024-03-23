from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Session, create_engine, select
from typing import Optional, List
from app.model.model import Job
from .model import CompanyRead
from .model import UserReadWithCompany
class JobRead(SQLModel):
    id: int
    title: str
    description: Optional[str]
    user_id: int
    maxSalary: int
    minSalary: int
    education: int
    # username : str

class Jobcreate(SQLModel):
    title: str
    maxSalary: int
    minSalary: int
    education: int
    description: str

class JobUpdate(SQLModel):
    maxSalary: Optional[int] = None
    minSalary: Optional[int] = None
    education: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None


class JobReadWithUser(JobRead):
    user: Optional[UserReadWithCompany] = None

class JobService:
    def __init__(self, session: Session):
        self.session = session

    def get_job(self, job_id: int) -> Job:
        job = self.session.get(Job, job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        return job

    def create_job(self, jobCreate: Jobcreate, user_id: int):
        db_job = Job.model_validate(jobCreate, update={"user_id": user_id}) # 从jobCreate创建一个从jobCreate创建一个Job实例，但忽略Job中没有的属性
        # 以下写法也可以
        # db_job = Job.model_validate(jobCreate)
        # db_job.user_id = user_id
        self.session.add(instance=db_job)
        self.session.commit()
        self.session.refresh(db_job)
        return db_job

    def update_job(self, job_id: int, jobUpdate: JobUpdate):
        job = self.session.get(Job, job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        # job_data.id = job_id
        job_data = jobUpdate.model_dump(exclude_unset=True) # 忽略属性值为None的字段
        job.sqlmodel_update(job_data)
        self.session.add(job)
        self.session.commit()
        self.session.refresh(job)
        return job_data

    def delete_job(self, job_id: int):
        job = self.session.get(Job, job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        self.session.delete(job)
        self.session.commit()
        return {"ok": True}
# app = FastAPI()