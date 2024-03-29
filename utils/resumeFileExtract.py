import base64
import re
from unittest import result
import requests
import json

def parseFile(fname =  u'1.docx' ,
    url = 'http://resumesdk.market.alicloudapi.com/ResumeParser' ):
    # 读取文件内容
    fileDir = "./upload"
    # cont = open(f'{fileDir}/{fname}', 'rb').read()
    cont = open(f'{fname}', 'rb').read()
    # base_cont = base64.b64encode(cont)  # python2
    base_cont = base64.b64encode(cont).decode('utf8')  # python3
        
    # 构造json请求
    data = {
            'file_name': fname,         # 简历文件名（需包含正确的后缀名）
            'file_cont': base_cont,     # 简历内容（base64编码的简历内容）
            'need_avatar': 0,            # 是否需要提取头像图片
            'ocr_type': 1,                 # 1为高级ocr
            }
    
    appcode = '393d056a692c43a199e021947c06b326'
    headers = {'Authorization': 'APPCODE ' + appcode,
               'Content-Type': 'application/json; charset=UTF-8',
               }
    # 发送请求
    data_js = json.dumps(data)
    res = requests.post(url=url, data=data_js, headers=headers)
    
    # 解析结果
    res_js = json.loads(res.text)
    print(json.dumps(res_js, indent=4, ensure_ascii=False))      # 打印全部结果
    # 保存结果
    if res_js['status']['code'] == 200:
        res_js['file_name'] = fname
        # with open( f'{fileDir}/{fname.replace('.pdf', '.json')}', 'w') as f:
        # with open( f'{fileDir}/'+fname.replace('.pdf', '.json'), 'w') as f:
        # with open(f'{fileDirfname+'.json'.replace('.doc', '.json'), 'w',encoding='utf8') as f:
        with open(fname+'.json'.replace('.doc', '.json'), 'w',encoding='utf8') as f:
        
        # with open("2.json", 'w') as f:
            #utf8编码，不转换为ascii编码
            f.write(json.dumps(res_js, indent=4, ensure_ascii=False))
            #保存

    return res_js

def convert_education(education):
    return {
        "school_name": education.get("edu_college", ""),
        "degree": education.get("edu_degree", ""),
        "date": [
            f"{education.get('start_date', '').replace('.','-')}-01T00:00:00.000Z",
            f"{education.get('end_date', '').replace('.','-')}-01T00:00:00.000Z"
        ],
        "major": education.get("major", ""),
        "main_courses": "",
        "ranking": "",
        "school_experience_description": ""
    }
    
def convert_project(project):
    return {
        "project_name": project.get("proj_name", ""),
        "project_role": project.get("proj_position", ""),
        "date": [
            f"{project.get('start_date', '').replace('.','-')}-01T00:00:00.000Z",
            f"{project.get('end_date', '').replace('.','-')}-01T00:00:00.000Z"
        ],
        "project_description": project.get("proj_content", "")
    }

def convert_work_experience(work_experience):
    return {
        "experience_name": work_experience.get("job_position", ""),
        "company_name": work_experience.get("job_cpy", ""),
        "date": [
            f"{work_experience.get('start_date', '').replace('.','-')}-01T00:00:00.000Z",
            f"{work_experience.get('end_date', '').replace('.','-')}-01T00:00:00.000Z"
        ],
        "location": "",
        "description": work_experience.get("job_content", "")
    }

def convert_skills(skills):
    return {
        "professional_skills": {
            "certificates": [],
            "description": [f"熟练掌握{skill.get('skills_name', '')}等技能" for skill in skills]
        }
    }
def convertFormate(res_js):
    result = res_js['result']
    
    personal_info = {
        "name": result.get('name', ''),
        # "birth_date": f"{result}-01T00:00:00.000Z",
        "sex": result.get('gender', result.get( "gender_inf", '')),
        "phone":result.get('phone', ''),
        # "email": result['email'],
        # "residence": result['address'],
    }
    education_experience = [convert_education(education) for education in result['education_objs']]
    
    professional_skills = convert_skills(result['skills_objs'])
    project_experience = [convert_project(project) for project in result['proj_exp_objs']]
    work_experience = [convert_work_experience(work_exp) for work_exp in result['job_exp_objs']]
    # 解析基本信息
    # TODO:根据不同的的输入简历返回的字段数据，人工修改数据结构转换函数
    resumeData = {
        "personal_info": personal_info,
        "education_experience": education_experience,
        "professional_skills": professional_skills,
        "project_experience": project_experience,
        "work_experience": work_experience ,
        "self_evaluation" : result.get("cont_my_desc", ""),    
        }
    return resumeData
# dict.get(key, default)
if __name__ == '__main__':
    url = 'http://resumesdk.market.alicloudapi.com/ResumeParser'
    fname = u'train_20200121\\resume_train_20200121\\0a2df74bbc31.pdf'
    res_js = parseFile()
    print(convertFormate(res_js))