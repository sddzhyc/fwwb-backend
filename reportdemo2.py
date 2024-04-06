from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet

def create_pdf(resume_data):
    c = canvas.Canvas("resume2.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    width, height = letter
    
    # Personal Info
    c.drawString(100, height - 50, f"Name: {resume_data['personal_info']['name']}")
    c.drawString(100, height - 65, f"Email: {resume_data['personal_info']['email']}")
    # Add more personal info fields as needed
    
    # Education History
    edu_y = height - 130
    c.drawString(100, edu_y, "Education History:")
    for edu in resume_data['education']:
        edu_y -= 15
        c.drawString(120, edu_y, f"{edu['degree']} - {edu['institution']} ({edu['year_start']} - {edu['year_end']})")
    
    # Project Experience
    proj_y = edu_y - 50
    c.drawString(100, proj_y, "Project Experience:")
    for proj in resume_data['projects']:
        proj_y -= 15
        c.drawString(120, proj_y, f"{proj['title']}: {proj['description']}")
    
    # Work Experience
    work_y = proj_y - 50
    c.drawString(100, work_y, "Work Experience:")
    for work in resume_data['work']:
        work_y -= 15
        c.drawString(120, work_y, f"{work['position']} - {work['company']} ({work['year_start']} - {work['year_end']})")
    
    # Personal Evaluation
    eval_y = work_y - 50
    c.drawString(100, eval_y, "Personal Evaluation:")
    c.drawString(120, eval_y - 15, resume_data['personal_evaluation'])
    
    c.save()

# Sample dictionary input:
resume_data = {
    'personal_info': {
        'name': 'John Doe',
        'email': 'john.doe@example.com'
    },
    'education': [
        {'degree': 'B.Sc. Computer Science', 'institution': 'University A', 'year_start': 2015, 'year_end': 2019}
    ],
    'projects': [
        {'title': 'Project Alpha', 'description': 'An innovative project solving X problem.'}
    ],
    'work': [
        {'position': 'Software Engineer', 'company': 'Tech Corp', 'year_start': 2019, 'year_end': 2022}
    ],
    'personal_evaluation': 'A highly motivated software engineer with a passion for solving complex problems.'
}

create_pdf(resume_data)
