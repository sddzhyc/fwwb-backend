from typing import Union , Optional

from pydantic import BaseModel
from fastapi import UploadFile, File, Response
from typing import List
# app = FastAPI()
from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from app.model import resume
from app.model.resume import Resume, ResumeCreate, ResumeResponse, ResumeService, ResumeUpdate
from app.routers.Login_v2 import get_current_active_user
from app.utils.noSQL import createClient
from ..model.model import User

router = APIRouter(
    # prefix="/resumes",
    tags=["resumes"],
    dependencies=[Depends(get_current_active_user)],
    responses={404: {"description": "Not found"}},
)


@router.post("/upload")
async def upload_file(file: UploadFile ):
    file_contents = await file.read()
    # 你可以在这里处理文件内容，例如保存到磁盘或者存储到数据库
    #保存到磁盘
    with open(f"upload/{file.filename}", "wb") as f:
        f.write(file_contents)
    return {"filename": file.filename}

@router.get("/resumes/", response_model= List[Resume])
def getMyResume(current_user: User = Depends(get_current_active_user)):
    
    service = ResumeService(createClient())
    
    return service.get_my_resume(current_user.id)


@router.get("/resumes/{resume_id}", response_model= Resume)
def getResume(resume_id: str, current_user: User = Depends(get_current_active_user)):
    
    service = ResumeService(createClient())
    
    return service.get_resume(resume_id=resume_id)

@router.post("/resumes/", response_model= ResumeResponse )
def createResume(resume: ResumeCreate, current_user: User = Depends(get_current_active_user)):
    
    service = ResumeService(createClient())
    
    return service.create_resume(resume, current_user.id)

@router.patch("/resumes/{resume_id}", response_model= Resume)
def updateResume(resume_id: str, resume: ResumeUpdate):
    
    service = ResumeService(createClient())
    
    return service.update_resume(resume_id, resume)

@router.delete("/resumes/{resume_id}")
def deleteResume(resume_id: str):
    
    service = ResumeService(createClient())
    
    return service.delete_resume(resume_id)