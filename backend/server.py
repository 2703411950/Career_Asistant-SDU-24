import requests
from flask import Flask, request, jsonify
import whisper
import base64
import zhconv
from paddleocr import PaddleOCR, draw_ocr
import datetime
import os
import fitz
import shutil
import random
from database import Database


from OCR import pyMuPDF_fitz
import json

from werkzeug.utils import secure_filename

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
app = Flask(__name__)


# 语音识别实例创建
model = whisper.load_model("base")
# 请求的URL
# RAG

# GLM3
url = 'http://127.0.0.1:7861/chat/file_chat'
url2 = 'http://127.0.0.1:7861/chat/chat'


# 语音上传
@app.route('/upload', methods=['POST'])
def upload_audio():
    try:
        data = request.json
        file_data = data['file']
        # 将base64编码的文件数据解码
        audio_data = base64.b64decode(file_data)
        # 将音频数据保存到文件
        with open('uploaded_file.wav', 'wb') as f:
            f.write(audio_data)
        # 使用Whisper模型进行语音识别
        result = model.transcribe('uploaded_file.wav', language='Chinese', fp16=False)
        texts = [segment["text"] for segment in result["segments"] if segment is not None]
        joined_text = ", ".join(texts)
        converted_text = zhconv.convert(joined_text, 'zh-cn')
        print(converted_text)
        # answer = Turing(converted_text)
        return jsonify({
            'code': 200,
            'result': converted_text
        })
    except Exception as e:
        return jsonify({'err_msg': str(e)}), 400


# 侧边栏表单上传文件上传：包含工作+公司+简历
@app.route('/upload_file', methods=['POST'])
def upload_file():
    job = request.form.get('job')
    company = request.form.get('company')
    interview = request.form.get('interview')
    f = request.files.get('file')
    # 如果文件不存在
    if f is None or f.filename == '':
        return jsonify({'code': 400, 'message': 'No file part in the request'}), 400
    # 保存文件
    fname = secure_filename(f.filename)  # 使用secure_filename来避免安全问题
    file_path = fname  # 这不是一个完整的路径，只是一个文件名
    try:
        f.save(file_path)  # 使用f.save而不是手动打开和写入文件
    except Exception as e:
        return jsonify({'code': 500, 'message': f'Failed to save file: {str(e)}'}), 500
        # 项目经历
    text = pyMuPDF_fitz(file_path, './img_tmp')
    if interview == "技术面":
        prompt = f"这是我的简历{text},请提取出我的软件项目经历，字数不超过600字"
    else:
        prompt = f"这是我的简历{text},请提取出我的荣誉奖项，校园经历，个人评价，字数不超过600字"
    extracted = Turing2(prompt)
    question = f"你是{company}公司的面试官，我要面试{job}岗位，现在要进行{interview},这是我的简历相关信息{extracted}，请你现在问5个面试问题，每个问题以问号结尾，确保每个问题一行"
    result = Turing(question)
    return jsonify({
        'code': 200,
        'result': result
    })


@app.route('/conclusion', methods=['POST'])
def conclude():
    data = request.json.get('memory')
    print(data)
    question = f"你是面试官，刚刚对我进行了面试，这是面试记录{data}，请你总结一下本次面试，并给我一些建议"
    result = Turing(question)
    return jsonify({
        'code': 200,
        'result': result
    })


# 与知识库对话
def Turing(text_words=""):
    # 准备请求体（JSON格式）
    payload = {
        "query": text_words,
        "knowledge_id": "tmpc1y1d30v",
        "top_k": 3,
        "score_threshold": 0.6,
        "history": [

        ],
        "stream": False,
        "model_name": "chatglm3-6b",
        "temperature": 0.7,
        "max_tokens": 0,
        "prompt_name": "default"
    }
    # 发送POST请求，并设置Content-Type为application/json
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=payload, headers=headers)

    # 检查响应状态码并打印响应内容
    if response.status_code == 200:
        json_str = response.text.split(': ', 1)[1]  # 使用split分割字符串，只取第二个部分（索引为1）
        try:
            # 解析JSON字符串
            data = json.loads(json_str)
            # 提取text字段的值
            text = data['answer']
            result = text.split('\n')
            # 输出分割后的数组（列表）
            print(result)
            return result
        except (json.JSONDecodeError, KeyError) as e:
            print('解析JSON或访问字段时出错:', e)
    else:
        print(f'请求失败，状态码：{response.status_code}')


# GLM3对话
def Turing2(text_words=""):
    # 准备请求体（JSON格式）
    payload = {
        "query": text_words,
        "conversation_id": "",  # 你可以根据需要设置此ID
        "history_len": -1,
        "history": [

        ],
        "stream": False,
        "model_name": "chatglm3-6b",
        "temperature": 0.7,
        "max_tokens": 0,  # 注意：max_tokens为0可能表示无限制，但具体取决于API的实现
        "prompt_name": "default"
    }

    # 发送POST请求，并设置Content-Type为application/json
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url2, json=payload, headers=headers)

    # 检查响应状态码并打印响应内容
    if response.status_code == 200:
        print('请求成功')
        json_str = response.text.split(': ', 1)[1]  # 使用split分割字符串，只取第二个部分（索引为1）
        try:
            # 解析JSON字符串
            data = json.loads(json_str)
            # 提取text字段的值
            text = data['text']
            print('文本内容:', text)
            return text
        except (json.JSONDecodeError, KeyError) as e:
            print('解析JSON或访问字段时出错:', e)
    else:
        print(f'请求失败，状态码：{response.status_code}')


def pyMuPDF_fitz(pdfPath, imagePath):
    startTime_pdf2img = datetime.datetime.now()  # 开始时间

    print("imagePath=" + imagePath)
    pdfDoc = fitz.open(pdfPath)
    for pg in range(pdfDoc.page_count):
        page = pdfDoc[pg]
        rotate = int(0)
        # 每个尺寸的缩放系数为4，这将为我们生成分辨率提高4的图像。
        # 此处若是不做设置，默认图片大小为：792X612, dpi=96
        zoom_x = 4  # (1.33333333-->1056x816)   (2-->1584x1224)
        zoom_y = 4
        mat = fitz.Matrix(zoom_x, zoom_y).prerotate(rotate)
        pix = page.get_pixmap(matrix=mat, alpha=False)

        if not os.path.exists(imagePath):  # 判断存放图片的文件夹是否存在
            os.makedirs(imagePath)  # 若图片文件夹不存在就创建

        pix.save(imagePath + '/' + 'images_%s.png' % pg)  # 将图片写入指定的文件夹内

    endTime_pdf2img = datetime.datetime.now()  # 结束时间
    print('pdf转图片时间=', (endTime_pdf2img - startTime_pdf2img).seconds)

    imgs = os.listdir(imagePath)
    page_list = []
    for img_name in imgs:
        absImagePath = os.path.join(imagePath, img_name)
        print(f"processing file: {absImagePath}")
        page_list.append(getContent(absImagePath))
    res = '\n'.join(page_list)
    # 检查文件夹是否存在
    if os.path.exists(imagePath):
        # 删除文件夹及其所有内容
        shutil.rmtree(imagePath)
        print(f"The folder {imagePath} and its contents have been successfully deleted.")
    else:
        print(f"The folder {imagePath} does not exist.")
    return res


def getContent(imagePath):
    result = ocr.ocr(imagePath, cls=True)
    experience = ''

    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            experience += line[1][0]
            experience += '\n'
    return experience


# 前端显示相应公司后端岗位的优秀面经
@app.route('/getExperienceWithOfset', methods=['POST'])
def showExperience():
    if request.method == "POST":
        company = request.json['data']['company']
        # 如果之后添加”前端“岗位，则应前端再传递一个”岗位“信息，从而到数据库中查询相应的数据
        job_list = request.json['data']['checkList']
        offset = request.json['data']['offset']
    if request.method == "GET":
        company = request.args.get['company']
        job_list = request.json['checkList']
        offset = request.json['offset']
    # 创建Database类的对象sql，test为需要访问的数据库名字 具体可见Database类的构造函数
    sql = Database("xmsx")
    try:
        #
        job_conditions = " OR ".join([f" job LIKE '%{job}%'" for job in job_list])
        result = sql.execute(
            f"SELECT title,content FROM companyandexperience WHERE company='{company}' AND ({job_conditions}) LIMIT {offset}, 1")
        print(result)
    except Exception as e:
        return {'status': "error", 'message': "code error"}
    else:
        if not len(result) == 0:
            # 返回查询结果，根据需要进行处理
            return jsonify({'status': 'success', 'title': result[0][0], 'content': result[0][1], })
        else:
            return {'status': 'success', 'title': "无", 'content': "空", }
            # return {'status':'error','message':'No matching record found'}
            # return {'status':'success','title':result[0][0],'content':result[0][1],}


# 根据公司岗位，这里的岗位是模糊查询，即算法、数据等类别，查询出公司要求，公司职责或描述
@app.route('/getCompanyJobInformationWithOfset', methods=['POST'])
def showCompanyJobInformationWithOfset():
    if request.method == "POST":
        company = request.json['data']['company']
        # 如果之后添加”前端“岗位，则应前端再传递一个”岗位“信息，从而到数据库中查询相应的数据
        job_list = request.json['data']['checkList']
        offset = request.json['data']['offset']
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
        return {'status': "error", 'message': "code error"}
    else:
        print(result)
        if not len(result) == 0:
            # 返回查询结果，根据需要进行处理
            return jsonify({'status': 'success', 'job': result[0][0], 'requirement': result[0][1], })
        else:
            return jsonify({'status': 'success', 'job': '无', 'requirement': '无'})
            # return {'status':'error','message':'No matching record found'}


@app.route('/getTechnicalQuestion', methods=['POST'])
def showTechnicalQuestion():
    if request.method == "POST":
        company = request.json['data']['company']
    if request.method == "GET":
        company = request.args.get['data']['company']
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
        return jsonify({'status': "error", 'message': "code error"})
    else:
        # print(result)
        if not len(result) == 0:
            # 返回查询结果，根据需要进行处理
            random_index1 = random.randint(0, len(result) - 1)
            random_index2 = random.randint(0, len(result) - 1)
            while random_index2 == random_index1:
                random_index2 = random.randint(0, len(result) - 1)
            # return {'status': 'success', 'question1': result[random_index1],'question2': result[random_index2]}
            return {'questions': [result[random_index1], result[random_index2]]}
        else:
            return {'status': 'success', 'question1': '无', 'question2': '无'}


if __name__ == '__main__':
    ocr = PaddleOCR(use_angle_cls=True, lang="ch")
    app.run(host='0.0.0.0', port=5000)
