from app.model.model import CompanyRead
from .model import Company, CompanyBase
from fastapi import HTTPException
from sqlmodel import SQLModel, Session, create_engine, select
from typing import Optional, List

class CompanyCreate(CompanyBase):
    name: str
    description: Optional[str] = None
    
class CompanyUpdate(CompanyBase):
    pass




#定义Company的CURD操作的类
class CompanyService:
    def __init__(self, session: Session):
        self.session = session

    def get_company(self, company_id: int) -> CompanyRead:
        company = self.session.get(Company, company_id)
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        return company

    def create_company(self, companyCreate: CompanyCreate):
        db_company = Company.model_validate(companyCreate)
        self.session.add(instance=db_company)
        self.session.commit()
        self.session.refresh(db_company)
        return db_company

    def update_company(self, company_id: int, companyUpdate: CompanyUpdate):
        company = self.session.get(Company, company_id)
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        company_data = companyUpdate.model_dump(exclude_unset=True)
        company.sqlmodel_update(company_data)
        self.session.add(company)
        self.session.commit()
        self.session.refresh(company)
        return company

    def delete_company(self, company_id: int):
        company = self.session.get(Company, company_id)
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        self.session.delete(company)
        self.session.commit()
        return company
