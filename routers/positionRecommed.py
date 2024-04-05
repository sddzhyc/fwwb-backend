from sqlmodel import desc, select, Session
from app.utils.db import get_session, getSession
from .Login_v2 import get_current_active_user
from app.model.model import User, Job
from typing import List
# from sqlmodel import Session

from fastapi import APIRouter, Depends, HTTPException, Query

router = APIRouter(
    # prefix="/evaluation",
    tags=["positionRecommed"],
    responses={404: {"description": "Not found"}},
)

# @router.post("/", response_model=List[JobRead])