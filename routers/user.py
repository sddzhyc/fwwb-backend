

from anyio import current_effective_deadline
from sqlmodel import Session
from app.model.job import JobUpdate
from app.model.model import User, UserRead, UserUpdate
from fastapi import APIRouter, Depends, HTTPException, Query

from app.model.user import UserService
from app.routers.Login_v2 import get_current_active_user
from app.utils.db import get_session

router = APIRouter(
    tags=["users"],
    # dependencies=[Depends(get_current_active_user)],
    responses={404: {"description": "Not found"}},
)
@router.patch("/{user_id}", response_model=UserRead)
def update_user(user_id: int, update: UserUpdate, current_user :User = Depends(get_current_active_user), session: Session = Depends(get_session)):
    if (user_id == current_user.id):
        userService = UserService(session) 
        return userService.updateUser(user_id, update)
    else:
        raise HTTPException(status_code=403, detail="You can only update your own user")

