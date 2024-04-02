from fastapi import FastAPI, HTTPException
from sqlmodel import Session, create_engine, select
from typing import List, Optional
from app.model.model import Job, JobBase
# from app.model.model import Job  # Import the Job class from the model module
from app.utils.db import getSession
from .model import CompanyRead
from .model import UserReadWithCompany
class JobRead(JobBase):
    id: int
    # description: Optional[str] = None
class Jobcreate(JobBase):
    pass

class JobUpdate(JobBase):
    maxSalary: Optional[int] = None
    jobType: Optional[int] = None
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
    
    def get_my_job(self, user_id: int) -> List[Job]:
        # session2 = getSession()
        # job = session2.exec(select(Job).where(Job.user_id == user_id)).first() 
        jobs = self.session.exec(select(Job).where(Job.user_id == user_id))
        #jobs转为list
        jobs = list(jobs)
        # print(jobs)
        if not jobs:
            raise HTTPException(status_code=404, detail="User not found")
        return jobs
    
    def create_jobs(self, jobCreateList: List[Jobcreate], user_id: int):
        db_jobList = []
        for jobCreate in jobCreateList:
            db_job = Job.model_validate(jobCreate, update={"user_id": user_id}) 
            self.session.add(instance=db_job)
            db_jobList.append(db_job)
        self.session.commit()  # 将提交移出循环
        for db_job in db_jobList:
            self.session.refresh(db_job)
        return db_jobList  # 返回整个列表，而不是最后一个元素

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

    def delete_job(self, job_id: int, current_user ):
        job = self.session.get(Job, job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        if current_user.id != job.user_id :
            raise HTTPException(status_code = 401, detail = "您没有删除权限！" )
        self.session.delete(job)
        self.session.commit()
        return {"ok": True}
# app = FastAPI()