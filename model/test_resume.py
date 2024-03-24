from fastapi.testclient import TestClient
from app.main import app
from app.model.resume import Resume, PersonalInfo, Education, Skill, Project
from app.utils.noSQL import createClient

client = TestClient(app)

def test_create_resume():
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
        resume_id=1
    )

    response = client.post("/resume/", json=resume.dict())
    assert response.status_code == 200
    assert response.json() == resume.dict()

def test_get_resume():
    response = client.get("/resume/1")
    assert response.status_code == 200
    assert response.json() == {
        "personal_info": {
            "name": "John Doe",
            "birth_date": "1990-01-01",
            "sex": "Male",
            "phone": "1234567890",
            "email": "john.doe@example.com",
            "residence": "New York"
        },
        "education_experience": [
            {
                "school_name": "University of ABC",
                "degree": "Bachelor's Degree",
                "start_date": "2010-09-01",
                "end_date": "2014-06-30",
                "major": "Computer Science",
                "main_courses": "Data Structures, Algorithms",
                "ranking": "First Class",
                "school_experience_description": "Lorem ipsum dolor sit amet"
            }
        ],
        "professional_skills": {
            "certificates": ["Certificate 1", "Certificate 2"],
            "description": ["Skill 1", "Skill 2"]
        },
        "project_experience": [
            {
                "project_name": "Project 1",
                "project_role": "Developer",
                "start_date": "2015-01-01",
                "end_date": "2016-12-31",
                "project_description": "Lorem ipsum dolor sit amet"
            }
        ],
        "user_id": 1,
        "resume_id": 1
    }

def test_update_resume():
    updated_resume = Resume(
        personal_info=PersonalInfo(
            name="John Doe",
            birth_date="1990-01-01",
            sex="Male",
            phone="1234567890",
            email="john.doe@example.com",
            residence="California"
        ),
        education_experience=[
            Education(
                school_name="University of XYZ",
                degree="Master's Degree",
                start_date="2015-09-01",
                end_date="2017-06-30",
                major="Computer Science",
                main_courses="Advanced Algorithms",
                ranking="Distinction",
                school_experience_description="Lorem ipsum dolor sit amet"
            )
        ],
        professional_skills=Skill(
            certificates=["Certificate 1", "Certificate 2", "Certificate 3"],
            description=["Skill 1", "Skill 2", "Skill 3"]
        ),
        project_experience=[
            Project(
                project_name="Project 2",
                project_role="Lead Developer",
                start_date="2017-01-01",
                end_date="2018-12-31",
                project_description="Lorem ipsum dolor sit amet"
            )
        ],
        user_id=1,
        resume_id=1
    )

    response = client.put("/resume/1", json=updated_resume.dict())
    assert response.status_code == 200
    assert response.json() == updated_resume.dict()

def test_delete_resume():
    response = client.delete("/resume/1")
    assert response.status_code == 200
    assert response.json() == 1from fastapi.testclient import TestClient
from app.main import app
from app.model.resume import Resume, ResumeService

client = TestClient(app)

def test_create_resume():
    resume_service = ResumeService()
    resume = Resume(
        personal_info=Resume.PersonalInfo(name="John Doe"),
        education_experience=[],
        professional_skills=Resume.Skill(certificates=[], description=[]),
        project_experience=[]
    )
    created_resume = resume_service.create_resume(resume)
    assert created_resume.user_id is not None

def test_get_resume():
    resume_service = ResumeService()
    user_id = 1
    resume = resume_service.get_my_resume(user_id)
    assert resume is not None
    assert resume.user_id == user_id

def test_update_resume():
    resume_service = ResumeService()
    user_id = 1
    updated_resume = Resume(
        personal_info=Resume.PersonalInfo(name="John Doe"),
        education_experience=[],
        professional_skills=Resume.Skill(certificates=[], description=[]),
        project_experience=[]
    )
    resume_service.update_resume(user_id, updated_resume)
    resume = resume_service.get_my_resume(user_id)
    assert resume is not None
    assert resume.user_id == user_id
    assert resume.personal_info.name == "John Doe"

def test_delete_resume():
    resume_service = ResumeService()
    user_id = 1
    resume_service.delete_resume(user_id)
    resume = resume_service.get_my_resume(user_id)
    assert resume is None