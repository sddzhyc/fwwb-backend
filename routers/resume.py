from typing import Union , Optional

from pydantic import BaseModel
from fastapi import HTTPException, UploadFile, File, Response
from typing import List
# app = FastAPI()
from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from sqlalchemy import exists

from app.model import resume
from app.model.resume import Resume, ResumeCreate, ResumeResponse, ResumeService, ResumeUpdate
from app.routers.Login_v2 import get_current_active_user
from app.utils.noSQL import createClient
from app.utils.resumeFileExtract import convertFormate, parseFile
from ..model.model import User

router = APIRouter(
    # prefix="/resumes",
    tags=["resumes"],
    dependencies=[Depends(get_current_active_user)],
    responses={404: {"description": "Not found"}},
)


@router.post("/upload")
async def upload_file(files: list[UploadFile] ):
    resumeDataList = []
    for file in files:
        if file.content_type not in ["application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"] :
            return Response(content={"message":"PDFs, doc, or docx only"}, status_code=422)
        file_contents = await file.read()
        # 你可以在这里处理文件内容，例如保存到磁盘或者存储到数据库
        #保存到磁盘
        with open(f"upload/{file.filename}", "wb") as f:
            f.write(file_contents)
        # 解析简历数据
        # TODO:开发测试阶段将解析简历数据的功能关闭
        # res_js = parseFile(f"upload/{file.filename}")
        # resumeData = convertFormate(res_js)
        # # 重新命名数据
        # resumeData["resume_name"] = file.filename
        # resumeDataList.append(resumeData)
    # return {"filenames": [file.filename for file in files]}
    return resumeDataList

@router.get("/resumes/", response_model= List[Resume])
def getMyResume(current_user: User = Depends(get_current_active_user)):
    
    service = ResumeService(createClient())
    
    return service.get_my_resume(current_user.id)


@router.get("/resumes/{resume_id}", response_model= Resume)
def getResume(resume_id: str, current_user: User = Depends(get_current_active_user)):
    
    service = ResumeService(createClient())
    #验证用户是否有权限查看
    exist_resume = service.get_resume(resume_id)
    if exist_resume.user_id != current_user.id:
        raise HTTPException(status_code = 401, detail = "您没有查看权限！" )
    return service.get_resume(resume_id=resume_id)

@router.post("/resumes/", response_model= ResumeResponse )
def createResume(resume: ResumeCreate, current_user: User = Depends(get_current_active_user)):
    
    service = ResumeService(createClient())
    
    return service.create_resume(resume, current_user.id)

@router.patch("/resumes/{resume_id}", response_model= Resume,)
def updateResume(resume_id: str, resumeUpdate: ResumeUpdate ,current_user: User = Depends(get_current_active_user)):
    
    service = ResumeService(createClient())
    #验证用户是否有权限修改
    exist_resume = service.get_resume(resume_id)
    if exist_resume.user_id != current_user.id :
        raise HTTPException(status_code = 401, detail = "您没有修改权限！" )
    #检查isPublic字段是否设为了True
    if resumeUpdate.isPublic == True and exist_resume.isPublic != True:

        resumeList = service.get_my_resume(current_user.id)
        for resume in resumeList:
            if resume.isPublic :
                resume.isPublic = False
                service.update_resume(resume.resume_id, resume)

    return service.update_resume(resume_id, resumeUpdate)

@router.delete("/resumes/{resume_id}")
def deleteResume(resume_id: str, current_user: User = Depends(get_current_active_user)):
    service = ResumeService(createClient())
    exist_resume = service.get_resume(resume_id)
    if exist_resume.user_id != current_user.id :
        raise HTTPException(status_code = 401, detail = "您没有删除权限！" )
    
    return service.delete_resume(resume_id)

@router.get("/resumes/getUserResume/{user_id}", response_model= Resume)
def getResume(user_id: int, current_user: User = Depends(get_current_active_user)):
    
    service = ResumeService(createClient())
    resumeList = service.get_my_resume(user_id)
    publicResume = None
    # 遍历，选取isPublic = True的resume
    for resume in resumeList:
        if resume.isPublic :
            publicResume = resume
            print(publicResume)
    if publicResume == None :
        raise HTTPException(status_code = 404, detail = "该用户没有公开的简历！" )

    return publicResume