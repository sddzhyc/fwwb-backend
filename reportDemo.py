from datetime import date
from turtle import title
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.graphics.shapes import Line
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
# 创建一个新的样式
# 注册字体
pdfmetrics.registerFont(TTFont('SimHei', 'SimHei.ttf'))

header_style = ParagraphStyle(
    'header_style',
    parent=getSampleStyleSheet()['Heading1'],
    fontName='SimHei',
    fontSize=13,
    # textColor='',
)

content_style = ParagraphStyle(
    'content_style',
    parent=getSampleStyleSheet()['BodyText'],
    fontName='SimHei',
    fontSize=12,
)

title_style = ParagraphStyle(
    'title_style',
    parent=getSampleStyleSheet()['Title'],
    fontName='SimHei',
    fontSize=13,
    alignment=1,
)
#日期格式：右对齐
date_style = ParagraphStyle(
    'date_style',
    parent=getSampleStyleSheet()['BodyText'],
    fontName='Helvetica',
    fontSize=12,
    alignment=2,
)
# 使用新的样式
doc = SimpleDocTemplate("resume.pdf", pagesize=letter)
story = []


data = {
  "resume_name": "0b3915da3907.pdf",
  "personal_info": {
    "name": "薛菲毓",
    "birth_date": None,
    "sex": "男",
    "phone": "13906890610",
    "email": None,
    "residence": None
  },
  "education_experience": [
    {
      "school_name": "北京市东城区职工业余大学",
      "degree": "大专",
      "date": [
        "2014-05-01T00:00:00.000Z",
        "2018-05-01T00:00:00.000Z"
      ],
      "major": "",
      "main_courses": "",
      "ranking": "",
      "school_experience_description": ""
    },
    {
      "school_name": "北京工业大学",
      "degree": "大专",
      "date": [
        "2012-10-01T00:00:00.000Z",
        "2016-10-01T00:00:00.000Z"
      ],
      "major": "软件工程",
      "main_courses": "数据结构、计算机网络、机器学习",
      "ranking": "",
      "school_experience_description": "获得国家奖学金"
    },
    {
      "school_name": "北京京北职业技术学院",
      "degree": "大专",
      "date": [
        "2009-06-01T00:00:00.000Z",
        "2013-06-01T00:00:00.000Z"
      ],
      "major": "",
      "main_courses": "",
      "ranking": "",
      "school_experience_description": ""
    }
  ],
  "professional_skills": {
    "certificates": None,
    "description": None
  },
  "project_experience": [
    {
      "project_name": "广州新岭南文化中心重点研究",
      "project_role": "",
      "link": None,
      "date": [
        "1990-06-01T00:00:00.000Z",
        "2012-07-01T00:00:00.000Z"
      ],
      "project_description": "1、负责组织、实施公司财务日常会计核算工作;2、负责集团组织架构梳理,合并报表编制,编写合并\n分析报告;3、负责指导、管理及检查下属各项目的会计核算管理;4、每月及时完成公司内部核算报表,\n编写分析报告;5、负责收集、整理、分析房地产行业各项税收政策,为集团及项目公司制定税收筹划\n方案;6、监控可能会对公司造成经济损失的重大经济活动;7、完成领导交办的其他任务。"
    },
    {
      "project_name": "学术研究",
      "project_role": "",
      "link": None,
      "date": [
        "2008-11-01T00:00:00.000Z",
        "2012-04-01T00:00:00.000Z"
      ],
      "project_description": "1、负责客户每月税控盘反写、以及税控盘保管和出入库登记;2、根据主管安排协助客户解决税盘问题;\n3、协助客户处理客户企业发票等相关事宜并根据客户情况统计开票记录,保管好相关物品,并进行相\n关登记4、协助会计做好每月单据等收集、装订及整理工作5、协助财务申报税、代理记账;6、协助办\n理公司变更、注销、设立7、其他财务类协助工作8、只招聘***。"
    },
    {
      "project_name": "理论研究",
      "project_role": "",
      "link": None,
      "date": [
        "1998-08-01T00:00:00.000Z",
        "2012-02-01T00:00:00.000Z"
      ],
      "project_description": "1、制作发货单据(如装车单/箱单等),确保信息传递准确及时;2、组织、管理散货的发运;3、管理\n后补件,安排发运;4、负责处理发货异常,并对异常信息进行收集、统计与分析;5、装运车辆的报到\n登记,保证装载顺序的有序进行;6、发布运输商考核信息;7、完成领导安排的其他工作。"
    }
  ],
  "work_experience": [
    {
      "experience_name": "置业顾问",
      "company_name": "陕西联盛企业管理咨询有限公司",
      "date": [
        "2004-09-01T00:00:00.000Z",
        "2018-10-01T00:00:00.000Z"
      ],
      "location": "",
      "description": "1、配合部门负责人整理、撰写各类文书、合同等文件。2、撰写项目建议书。3、整理部门票据,提交\n部门费用报销等事宜。4、能够适应短期周边出差。5、领导安排的其他工作。"
    },
    {
      "experience_name": "营销储备干部7500起",
      "company_name": "好家网络科技有限公司",
      "date": [
        "1992-03-01T00:00:00.000Z",
        "2013-04-01T00:00:00.000Z"
      ],
      "location": "",
      "description": "1、负责统计仓库人员考勤;2、仓库货品出入库统计;3、作业单据的准确开制、确认、交接及打印;"
    }
  ],
  "isPublic": False,
  "self_evaluation": "本人对工作持积极认真的态度,责任心强,为人诚恳、细心、稳重,有良好的团队精神,能快速适应工\n作环境,并能在实际工作中不断学习,不断提高自身的能力与综合素质,不断完善自己,做好本职工作。",
  "user_id": 2,
  "resume_id": "6608d231ddee1a79c9a45af4"
}

def addExperience(experiences):
    # 创建一条线
    # line = Line(0, 0, 7.5*inch, 0)
    # 添加到故事中
    # story.append(line)
    story.append(Paragraph("工作经历", header_style))
    for experience in experiences:
        
        story.append(Paragraph(experience.get("experience_name"), content_style))
        #公司名称
        story.append(Paragraph(experience.get('company_name'), content_style))
        story.append(Paragraph(f"{experience.get('date')[0][:7]} - {experience.get('date')[0][:7]}", content_style))
        story.append(Paragraph("Developed and maintained software applications.", content_style))
        #角色
        # story.append(Paragraph(experience, content_style))
        story.append(Paragraph(experience.get('description'), content_style))
        #个人描述
        story.append(Spacer(1, 12))
    # story.append(Paragraph("Work Experience", header_style))
    # story.append(Paragraph(experience.school_name, content_style))
    # story.append(Paragraph(experience.degree, content_style))
    # story.append(Paragraph(f"{experience.start_date} - {experience.end_date}", content_style))
    # story.append(Paragraph(experience.major, content_style))
    # story.append(Paragraph(experience.main_courses, content_style))
    # story.append(Paragraph(experience.ranking, content_style))
    # story.append(Paragraph(experience.school_experience_description, content_style))
    story.append(Spacer(1, 12))

addExperience(data['work_experience'])

# # 添加个人信息
# story.append(Paragraph("John Doe", header_style))
# story.append(Paragraph("123 Main St, Anytown, USA", content_style))
# story.append(Paragraph("john.doe@example.com", content_style))
# story.append(Spacer(1, 12))

# # 添加教育背景
# story.append(Paragraph("Education", header_style))
# story.append(Paragraph("Bachelor of Science in Computer Science, Any University, 2015-2019", content_style))
# story.append(Spacer(1, 12))

# # 添加工作经历

# story.append(Paragraph("Software Engineer, Some Company, 2019-present", content_style))
# story.append(Paragraph("Responsibilities:", content_style))
# story.append(Paragraph("Developed and maintained software applications.", content_style))

# 生成PDF
doc.build(story)