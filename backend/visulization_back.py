from flask import Flask,render_template,request
from database import Database
from flask_cors import CORS
import random
import pymysql

# 实例化一个flask对象，
app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "hello"
# 前端显示相应公司后端岗位的优秀面经
@app.route('/api/getExperienceWithOfset',methods=['POST'])
def showExperience():
    if request.method == "POST":
        company = request.json['company']
        # 如果之后添加”前端“岗位，则应前端再传递一个”岗位“信息，从而到数据库中查询相应的数据
        job_list = request.json['checkList']
        offset = request.json['offset']
    if request.method == "GET":
        company = request.args.get['company']
        job_list = request.json['checkList']
        offset = request.json['offset']
    # 创建Database类的对象sql，test为需要访问的数据库名字 具体可见Database类的构造函数
    sql = Database("xmsx")
    try:
        #
        job_conditions = " OR ".join([f" job LIKE '%{job}%'" for job in job_list])
        result = sql.execute(f"SELECT title,content FROM companyandexperience WHERE company='{company}' AND ({job_conditions}) LIMIT {offset}, 1")
        print(result)
    except Exception as e:
        return {'status':"error", 'message': "code error"}
    else:
        if not len(result) == 0:
            #返回查询结果，根据需要进行处理
            return {'status':'success','title':result[0][0],'content':result[0][1],}
        else:
            return {'status':'success','title':"无",'content':"空",}
            # return {'status':'error','message':'No matching record found'}
            # return {'status':'success','title':result[0][0],'content':result[0][1],}

# 根据公司岗位，这里的岗位是模糊查询，即算法、数据等类别，查询出公司要求，公司职责或描述
@app.route('/api/getCompanyJobInformationWithOfset',methods=['POST'])
def showCompanyJobInformationWithOfset():
    if request.method == "POST":
        company = request.json['company']
        # 如果之后添加”前端“岗位，则应前端再传递一个”岗位“信息，从而到数据库中查询相应的数据
        job_list = request.json['checkList']
        offset = request.json['offset']
    if request.method == "GET":
        company = request.args.get['company']
        job_list = request.args.get['checkList']
        offset = request.args.get['offset']
    # 创建Database类的对象sql，test为需要访问的数据库名字 具体可见Database类的构造函数
    sql = Database("xmsx")
    try:
        # 构建SQL查询语句，使用LIKE和OR关键字进行模糊匹配
        job_conditions = " OR ".join([f"job_name LIKE '%{job}%'" for job in job_list])
        sql_query = f"SELECT job_name, job_require FROM companyandjob WHERE company='{company}' AND ({job_conditions}) LIMIT {offset}, 1"
        result = sql.execute(sql_query)
        print(result)
    except Exception as e:
        return {'status':"error", 'message': "code error"}
    else:
        print(result)
        if not len(result) == 0:
            #返回查询结果，根据需要进行处理
            return {'status':'success','job':result[0][0],'requirement':result[0][1],}
        else:
            return {'status':'success','job':'无','requirement':'无'}
            # return {'status':'error','message':'No matching record found'}

@app.route('/api/getTechnicalQuestion',methods=['POST'])
def showTechnicalQuestion():
    if request.method == "POST":
        company = request.json['company']
    if request.method == "GET":
        company = request.args.get['company']
        # 创建Database类的对象sql，test为需要访问的数据库名字 具体可见Database类的构造函数
    sql = Database("xmsx")
    try:
        # 首先查询相应公司前10个关键词
        keywords_query = sql.execute(
            f"SELECT keyword FROM keyword WHERE company='{company}' ORDER BY frequence DESC LIMIT 10")
        keywords = [keyword[0] for keyword in keywords_query]

        keyword_conditions = " OR ".join([f"content LIKE '%{keyword}%'" for keyword in keywords])
        result = sql.execute(f"SELECT content FROM technical_question WHERE {keyword_conditions}")
        # print(result)  # 调试信息：打印查询结果

    except Exception as e:
        print(e)  # 调试信息：打印异常信息
        return {'status': "error", 'message': "code error"}
    else:
        # print(result)
        if not len(result) == 0:
            # 返回查询结果，根据需要进行处理
            random_index1 = random.randint(0,len(result) - 1)
            random_index2 = random.randint(0,len(result) - 1)
            while random_index2 == random_index1:
                random_index2 = random.randint(0,len(result) - 1)
            # return {'status': 'success', 'question1': result[random_index1],'question2': result[random_index2]}
            return {'questions':[result[random_index1],result[random_index2]]}
        else:
            return {'status': 'success', 'question1': '无','question2':'无'}
            # return {'status': 'error', 'message': 'No matching record found'}




app.run(port=8085,debug=True)
# debug==True是为了方便修改代码之后，能够不重启项目就能够更新，否则，每次更改代码都需要重新启动项目
