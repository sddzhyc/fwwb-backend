from sqlmodel import desc, select, Session
from app.model.evalution import EvaluationRequest, EvaluationResponse
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
    
    return req