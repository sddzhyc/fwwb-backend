from ..model.company import CompanyCreate, CompanyUpdate, CompanyService



from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.utils.db import getSession
from typing import List
from ..model.model import CompanyRead, UserReadWithCompany
from ..model.company import CompanyService

#实现Company的CURD操作
router = APIRouter()
# @router.get("/company", response_model=List[CompanyRead])
# def get_companies(skip: int = 0, limit: int = 100, db: Session = Depends(getSession)):
#     companies = CompanyService.get_company(db, skip=skip, limit=limit)
#     return companies

@router.get("/companies/{company_id}", response_model=CompanyRead)
def get_company(company_id: int, session: Session = Depends(getSession)):
    service = CompanyService(session)
    company = service.get_company( company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@router.post("/companies", response_model=CompanyRead)
def create_company(company: CompanyCreate, db: Session = Depends(getSession)):
    service = CompanyService(db)
    created_company = service.create_company(company)
    return created_company

@router.patch("/companies/{company_id}", response_model=CompanyRead)
def update_company(company_id: int, company: CompanyUpdate, db: Session = Depends(getSession)):
    service = CompanyService(db)
    updated_company = service.update_company( company_id, company)
    if not updated_company:
        raise HTTPException(status_code=404, detail="Company not found")
    return updated_company

@router.delete("/companies/{company_id}")
def delete_company(company_id: int, db: Session = Depends(getSession)):
    service = CompanyService(db)
    deleted_company = service.delete_company(company_id)
    if not deleted_company:
        raise HTTPException(status_code=404, detail="Company not found")
    return {"message": "Company deleted successfully"}