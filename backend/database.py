import pymysql

class Database:
    # 设置数据库连接
    host='localhost'
    user='root'
    password = "123456"
    def __init__(self,db):
        connect=pymysql.connect(host=self.host,user=self.user,password=self.password,db=db)
        self.cursor = connect.cursor()
    # 执行sql语句
    def execute(self,command):
        try:
            # 执行command中的sql语句
            self.cursor.execute(command)
        except Exception as e:
            return e
        else:
            return self.cursor.fetchall()