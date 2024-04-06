from sqlmodel import desc, select, Session
from app.model.evalution import EvaluationRequest, EvaluationResponse
from app.model.resume import ResumeBase
from app.utils.db import get_session, getSession
from .Login_v2 import get_current_active_user
from app.model.model import User, Job
from typing import List
# from sqlmodel import Session

from fastapi import APIRouter, Depends, HTTPException, Query
router = APIRouter(
    # prefix="/evaluation",
    tags=["evaluation"],
    responses={404: {"description": "Not found"}},
)

@router.post("/getEvaluation", response_model=EvaluationRequest)
def getEvaluation(req :EvaluationRequest, session: Session = Depends(get_session)):
    resumeData  : ResumeBase = req.resume

    project_experience = resumeData.project_experience
    work_experience = resumeData.work_experience
    inputData = ""
        #项目描述和工作内容拼接一个大字符串
    if project_experience:
        for project in project_experience:
            if project.project_description:
                inputData += project.project_description

    if work_experience:
        for work in work_experience:
            if work.description:
                inputData += work.description
    
    return inputData