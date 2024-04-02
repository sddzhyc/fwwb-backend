from hmac import new
from os import link
import re
from tkinter import N
from typing import List, Optional
# from sqlmodel import SQLModel, Field
from pydantic import BaseModel
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
# from app.model import user
# from app.utils.noSQL import createClient
from fastapi import HTTPException
from bson.objectid import ObjectId
from sqlalchemy import false
from app.model import company
from app.routers import resume
from app.utils.encrypt import CrypteService

def createClient():
    # uriDemo = "mongodb+srv://root:<password>@demo.mysl5zj.mongodb.net/"
    uri = "mongodb+srv://root:lmsCAoHCBpDYxdgs@demo.mysl5zj.mongodb.net/?retryWrites=true&w=majority&appName=demo"
    secret = "lmsCAoHCBpDYxdgs"
# Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    return client

class PersonalInfo(BaseModel):
    name: Optional[str] = None
    birth_date: Optional[str] = None
    sex: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    residence: Optional[str] = None

class Education(BaseModel):
    school_name: Optional[str] = None
    degree: Optional[str] = None
    date : Optional[List[str]] = None
    major: Optional[str] = None
    main_courses: Optional[str] = None
    ranking: Optional[str] = None
    school_experience_description: str

class Skill(BaseModel):
    certificates: Optional[List[str]] = None
    description: Optional[List[str]] = None

class Project(BaseModel):
    project_name: Optional[str] = None
    project_role: Optional[str] = None
    link: Optional[str] = None
    date : Optional[List[str]] = None
    project_description: Optional[str] = None

class WorkExperience(BaseModel):
    experience_name: Optional[str] = None
    company_name: Optional[str] = None
    date : Optional[List[str]] = None
    location : Optional[str] = None
    description: Optional[str] = None

class ResumeBase(BaseModel):
    resume_name : Optional[str] = None
    personal_info: Optional[PersonalInfo] = None
    education_experience: Optional[List[Education]] = None
    professional_skills: Optional[Skill] = None
    project_experience:  Optional[List[Project]] = None
    work_experience : Optional[List[WorkExperience]] = None
    isPublic : Optional[bool] = False
    #个人评价
    self_evaluation: Optional[str] = None
class Resume(ResumeBase):
    # user_id: Optional[int] = None
    user_id: int
    resume_id : Optional[str] = None  # 用于区分同一用户的简历（需要吗？） 
    # _id : str # 不要命名为_id, 否则会被看作是私有成员变量！
class ResumeCreate(ResumeBase):
    user_id: Optional[int] = None 
class ResumeUpdate(ResumeBase):
    pass

class ResumeResponse(BaseModel):
    resume_id : str
    isAknowledged : bool

class ResumeService:
    def __init__(self, client ) -> None:
        self.client = client
        self.db = client["fwwb"]
        # self.collection = self.db["resume"]
        self.collection = self.db["resume_encrypted"]
    
    def create_resume(self, resume: ResumeCreate, user_id : int):
        #TODO:(已解决？)实现不把user_id设为Optional就可验证的方法
        # resume.user_id = user_id
        resumeData = resume.model_dump()
        resumeData["user_id"] = user_id
        # print("type:",user_id,type(user_id))
        db_resume = Resume.model_validate(resumeData)
        # db_resume.user_id = user_id
        db_resumeData = db_resume.model_dump()
        # 加密
        crypteService = CrypteService()
        db_resumeData_encrypted = crypteService.encrypt_dict(db_resumeData)
        
        InsertOneResult = self.collection.insert_one(db_resumeData_encrypted)
        res = ResumeResponse(resume_id = str(InsertOneResult.inserted_id), isAknowledged = InsertOneResult.acknowledged)
        return res
    
    def get_my_resume(self, user_id: int) -> List[Resume]:
        resumes_cursor = self.collection.find({"user_id": user_id})
        if resumes_cursor:
            resumes : List[Resume] = [] 
            for resume_encrypted in resumes_cursor: #修改resume 不会修改resumes_cursor！！！
                #解密
                crypteService = CrypteService()
                resume = crypteService.decrypt_dict(resume_encrypted)
                resume["resume_id"] = str(resume["_id"]) # 将ObjectId转为str
                resumes.append(Resume.model_validate(resume))
            # resumes = [Resume.model_validate(resumeData) for resumeData in resumes_cursor]
            # print("resumes:",resumes)
            return resumes
        else:
            raise HTTPException(status_code=404, detail="Resume not found")

    def get_resume(self, resume_id: str):
        id_to_find = ObjectId(resume_id)
        resume_encrypted = self.collection.find_one({"_id": id_to_find})
        #解密
        crypteService = CrypteService()
        resume = crypteService.decrypt_dict(resume_encrypted)
        # print("resume:",resume)
        if resume:
            resume["resume_id"] = str(resume["_id"])
            resumeClass = Resume(**resume)
            print("resumeClass:",resumeClass)
            return resumeClass
        else:
            raise HTTPException(status_code=404, detail="Resume not found")
    
    #TODO:（该问题前端已解决）目前会修改所有字段，需要修改为只修改传入的字段
    def update_resume(self, resume_id: str, resume: ResumeUpdate):
        
        id_to_find = ObjectId(resume_id)
        existing_resume = self.collection.find_one({"_id": id_to_find})
        if existing_resume:
            # 加密
            crypteService = CrypteService()
            db_resumeData_encrypted = crypteService.encrypt_dict(resume.model_dump())
            self.collection.update_one({"_id": id_to_find}, {"$set": db_resumeData_encrypted})
            ResumeUpdated = self.get_resume(id_to_find)
            return ResumeUpdated
        else:
            raise HTTPException(status_code=404, detail="Resume not found")
    
    def delete_resume(self, resume_id: str):
        id_to_find = ObjectId(resume_id)
        result = self.collection.delete_one({"_id": id_to_find})
        if result.deleted_count > 0:
            return {"message": "Resume deleted successfully", "resume_id": resume_id}
        else:
            raise HTTPException(status_code=404, detail="Resume not found")



#test
def test():
    resume = Resume(
            personal_info=PersonalInfo(
                name="John Doe",
                birth_date="1990-01-01",
                sex="Male",
                phone="1234567890",
                email="john.doe@example.com",
                residence="New York"
            ),
            education_experience=[
                Education(
                    school_name="University of ABC",
                    degree="Bachelor's Degree",
                    start_date="2010-09-01",
                    end_date="2014-06-30",
                    major="Computer Science",
                    main_courses="Data Structures, Algorithms",
                    ranking="First Class",
                    school_experience_description="Lorem ipsum dolor sit amet"
                )
            ],
            professional_skills=Skill(
                certificates=["Certificate 1", "Certificate 2"],
                description=["Skill 1", "Skill 2"]
            ),
            project_experience=[
                Project(
                    project_name="Project 1",
                    project_role="Developer",
                    start_date="2015-01-01",
                    end_date="2016-12-31",
                    project_description="Lorem ipsum dolor sit amet"
                )
            ],
            user_id=1,
            # resume_id
        )

    service = ResumeService(createClient())

    result = service.create_resume(resume, 2)
    print("create_resume:", result)
    print()
    print("get_resume:", service.get_my_resume(1))
    print()
    resume.personal_info.sex = "girl"
    print("update_resume:", service.update_resume(1, resume))
    print()
    print("delete_resume:", service.delete_resume(1))

if __name__ == "__main__":
    test()