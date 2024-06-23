from flask import Flask,render_template,request
from database import Database
from flask_cors import CORS
import pymysql

# 实例化一个flask对象，
app = Flask(__name__)
CORS(app)
# 路由 test用
@app.route('/')
def showGoodExperience():
    return render_template("index.html")

@app.route('/data')
def data():
    return render_template("data.html")

#根据岗位，公司，查询 岗位要求，岗位描述   以在前端显示卡片形式的公司信息
@app.route('/show',methods=['GET','POST'])
def show():
    #首先获取前端传入的company数据
    if request.method == "POST":
        job = request.form.get("name")
    if request.method == "GET":
        job = request.args.get['name']
        # job = request.json['job']

    #创建Database类的对象sql，test为需要访问的数据库名字 具体可见Database类的构造函数
    sql = Database("xmsx")
    try:
        #执行sql语句 多说一句，f+字符串的形式，可以在字符串里面以{}的形式加入变量名 结果保存在result数组中
        result = sql.execute(f"SELECT company FROM companyandjob WHERE job_name='{job}' ")
    except Exception as e:
        return {'status':"error", 'message': "code error"}
    else:
        if not len(result) == 0:
            #返回查询结果，根据需要进行处理
            return {'status':'success','message':result[0][0]}
        else:
            return {'status':'error','message':'No matching record found'}

# # 进入页面则调用此函数，此函数查询数据库中公司岗位信息前30条记录，前端接受到公司岗位信息后可显示在卡片中，实现可视化
# @app.route('/show', methods=['GET'])
# def showCompanyAndJob():
#     # 创建 Database 类的对象 sql，test 为需要访问的数据库名字，具体可见 Database 类的构造函数
#     sql = Database("xmsx")
#     try:
#         # 执行 SQL 查询语句，获取前30条记录
#         result = sql.execute("SELECT * FROM companyandjob LIMIT 30")
#     except Exception as e:
#         return {'status': 'error', 'message': 'code error'}
#     else:
#         if len(result) > 0:
#             # 返回查询结果，根据需要进行处理
#             return {'status': 'success', 'data': result}
#         else:
#             return {'status': 'error', 'message': 'No matching record found'}
#
# 前端显示相应公司后端岗位的优秀面经
@app.route('/api/getExperienceWithOfset',methods=['POST'])
def showExperience():
    if request.method == "POST":
        company = request.json['company']
        # 如果之后添加”前端“岗位，则应前端再传递一个”岗位“信息，从而到数据库中查询相应的数据
        job = request.json['job']
        offset = request.json['offset']
    if request.method == "GET":
        company = request.args.get['company']
        job = request.json['job']
        offset = request.json['offset']
    # 创建Database类的对象sql，test为需要访问的数据库名字 具体可见Database类的构造函数
    sql = Database("xmsx")
    try:
        title_list = []
        # 这里可以写死几个好的面经的title
        if company == '阿里':
            title_list = ['五⾯阿⾥,终获offer',]
        if company =='华为':
            title_list = ['华为面经分享']
        if company =='腾讯':
            title_list =['腾讯面经分享']
        #执行sql语句 f+字符串的形式，可以在字符串里面以{}的形式加入变量名 结果保存在result数组中
        result = sql.execute(f"SELECT title,content FROM companyandexperience WHERE company='{company}' AND title IN {tuple(title_list)} LIMIT 1 OFFSET {offset} ")
    except Exception as e:
        return {'status':"error", 'message': "code error"}
    else:
        if not len(result) == 0:
            #返回查询结果，根据需要进行处理
            return {'status':'success','title':result[0][0],'content':result[0][1],}
        else:
            return {'status':'error','message':'No matching record found'}




app.run(port=8080,debug=True)
# debug==True是为了方便修改代码之后，能够不重启项目就能够更新，否则，每次更改代码都需要重新启动项目
