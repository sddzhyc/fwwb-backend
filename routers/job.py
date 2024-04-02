from sqlmodel import desc, select, Session
from app.model.job import JobRead, JobReadWithUser, JobService, JobUpdate, Jobcreate
from app.utils.db import get_session, getSession
from .Login_v2 import get_current_active_user
from app.model.model import User, Job
from typing import List
# from sqlmodel import Session

from fastapi import APIRouter, Depends, HTTPException, Query
router = APIRouter()

@router.get("/jobs/", response_model=List[JobRead])
def read_jobs(offset: int = 0, limit: int = Query(default=100, le=100)):
    with getSession() as session:
        jobes = session.exec(select(Job).offset(offset).limit(limit)).all()
        return jobes


@router.post("/jobs/", response_model=List[JobRead])
# 使用Depends获取session
def create_job(*, jobCreateList: List[Jobcreate], current_user: User = Depends(get_current_active_user),session = Depends(get_session)):

    # job.username = current_user.username
    # with get_session() as session:
    service = JobService(session)
    # print(current_user.id)
    return service.create_jobs(jobCreateList, current_user.id) # type: ignore

@router.get("/jobs/{job_id}", response_model=JobReadWithUser)
def read_job(job_id: int, session: Session = Depends(get_session)):
# def read_job(job_id: int, ):
    # 这么写在提取user时会报错？
    # return service.get_job(job_id)
    service = JobService(session)
    job = service.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Hero not found")
    return job

@router.get("/my_jobs/", response_model=List[JobRead])
def get_my_job(current_user: User = Depends(get_current_active_user),session = Depends(get_session)):

    service = JobService(session)
    # print(current_user.id)
    return service.get_my_job(current_user.id) # type: ignore
# @router.patch("/jobs/{job_id}", response_model=JobRead)
# def update_job(job_id: int, job: JobUpdate):
#     print(job.description)
#     with getSession() as session:
#         service = JobService(session)
#         return service.update_job(job_id, job)

@router.patch("/jobs/{job_id}", response_model=JobRead)
def update_job(job_id: int, job: JobUpdate, current_user: User = Depends(get_current_active_user)):
    with getSession() as session:
        # print(JobUpdate.description) 
        db_job = session.get(Job, job_id)
        if not db_job:
            raise HTTPException(status_code=404, detail="job not found")
        if current_user.id != db_job.user_id :
            raise HTTPException(status_code = 401, detail = "您没有修改权限！" )
        job_data = job.model_dump(exclude_unset=True)
        db_job.sqlmodel_update(job_data)
        session.add(db_job)
        session.commit()
        session.refresh(db_job)
        return db_job

@router.delete("/jobs/{job_id}", )
def delete_job(job_id: int, current_user: User = Depends(get_current_active_user)):
    with getSession() as session:
        service = JobService(session)
        return service.delete_job(job_id, current_user)
