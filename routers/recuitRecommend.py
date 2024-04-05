import re
from copier import Optional
from sqlmodel import desc, select, Session
from app.database import Base
from app.model import user
from app.model.job import JobService
from app.utils.db import get_session, getSession
from .Login_v2 import get_current_active_user
from app.model.model import User, Job
from typing import List
# from sqlmodel import Session

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
router = APIRouter(
    # prefix="/evaluation",
    tags=["recuitRecommed"],
    responses={404: {"description": "Not found"}},
)
class RecommedUserInfo(BaseModel):
    user_id: int
    username: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None

class recuitRecommed(BaseModel):
    # userInfo : RecommedUserInfo
    key: int
    user_id: int
    username: Optional[str] = None
    email: Optional[str] = None
    telephone: Optional[str] = None
    full_name: Optional[str] = None
    #匹配度
    matchRate: float
    tags : List[str] = []

@router.get("/recuit_recommed", response_model=List[recuitRecommed])
def getRecuitRecommed(jobId :int, session: Session = Depends(get_session), current_user: User = Depends(get_current_active_user)):
    #获取job信息
    jobService = JobService(session)
    job = jobService.get_job(jobId)
    # 创建 RecommedUserInfo 实例
    # user_info = RecommedUserInfo(user_id=1, username="user1", email="user1@example.com", full_name="User One")

    # 创建 recuitRecommed 实例
    recuit_recommed = recuitRecommed(user_id=2, key=1,username="user1", email="user1@example.com", full_name="User One", matchRate=0.85)
    res = [recuit_recommed]
    return res