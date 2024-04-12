

from anyio import current_effective_deadline
from sqlmodel import Session
from app.model.job import JobUpdate
from app.model.model import User, UserCreate, UserRead, UserReadWithCompany, UserUpdate
from fastapi import APIRouter, Depends, HTTPException, Query

from app.model.user import UserService, createUser
from app.routers.Login_v2 import get_current_active_user
from app.routers.Login_v2 import get_password_hash
from app.utils.db import get_session

router = APIRouter(
    tags=["users"],
    # dependencies=[Depends(get_current_active_user)],
    responses={404: {"description": "Not found"}},
)
@router.patch("/user", response_model=UserRead)
def update_user(update: UserUpdate, current_user :User = Depends(get_current_active_user), session: Session = Depends(get_session)):
    userService = UserService(session) 
    #密码转为哈希值
    update.password = get_password_hash(update.password)
    return userService.updateUser(current_user.id, update)

@router.post("/register", response_model=UserRead)
def register(user: UserCreate):
    user.password = get_password_hash(user.password)
    return createUser(user)


@router.get("/users/me", response_model=UserReadWithCompany)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    # print(current_user)
    return current_user