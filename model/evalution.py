from turtle import position
from typing import List, Optional
# from sqlmodel import SQLModel, Field
from pydantic import BaseModel
# 
from app.model.resume import ResumeBase

class ExcepetPosition(BaseModel):
    jobType: int # 职位类型id
    maxSalary: int
    minSalary: int
    education: int #    
    positionType: Optional[int] = None #职位类型id
    location : Optional[int] = None #工作地点，代码(具体到城市)
    # tags : Optional[str] = None  #职位标签，json格式的数组序列化后存储

class EvaluationRequest(BaseModel):
    resume : ResumeBase
    exceptPosition : ExcepetPosition

class EvaluationResponse(BaseModel):
    pass
    # score : float
    # jobList : List[ExcepetPosition]