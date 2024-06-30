import csv
import jieba
from wordcloud import WordCloud
from matplotlib import pyplot as plt
from PIL import Image
import numpy as np
from collections import defaultdict

file_object2 = open(r'D:\大三下\课程\项目实训\任务\16第16周\字节跳动\字节跳动.csv',encoding='utf-8').read().split('\n')  # 一行行的读取内容
stop_words = ['一个', '实现', '数据', '什么', '通过', '使用', '解决', '方法',
              '问题', '请求', '可以',"可能","怎么","进行","主要","执行","多个",
              "每个","如果","类型","时间","需要","区别","控制","一下","一种",
              "哪些","创建","元素","如何","一定","用于","避免","应用","设计","原理",
              "了解","不同","提供","以下","相关","处理","资源","时候","没有","导致","基于","优化",
              "用户","然后","包括","面试","场景","运行","方式","根据","固定","操作","配置",
              "策略","基本","从而","所有","分别","情况","常见","不是","开始","一些","实例","存在","其他",
              "这种","介绍","存在","保证","允许","全部","设置","整个","还有","为什么","简单","面试官","级别",
              "之间","发生","表示","输出","输入","任务","int","题解","统一","考试","100","给定","数量","长度",
              "两个","遍历","小朋友","其中","计算","整数","空格","200","题目","200","代表","最大","这个","最小",
              "第一行","返回","例如","员工","思路","第二行","我们","行为","披萨","正整数","范围","出现",
              "地图","汽车","解题","大小","位置","个数","月饼","基站","new","过程","ren","元音","玩家","初始","是否","找到",
              "10","static","最后","if","棋盘","要求","频次","方案","城市","同时","结果","public","到达","接下来","属于",
              "按照","组成","最长","这是","相同","小于","记录","get","项目","java","实习","二面","一面","自己","大量","反问",
              "小美","测试","仅供参考","感觉","拷打","不会","部门","糖果","驶入","休息区","11","机制","火车","驶出","以及","直接","还是",
              "13","12","对于","14","15","分钟","具体","时刻","学习","因为","知道","出口","一道","重复","自我介绍","美团","顺序","每次",
              "任意","多少","所以","就是","笔试","回答","...","但是","参考","选择","简历","确保","分析","腾讯","四次","这些",
              "偏爱","参考答案","修改","查找","通常","压缩","访问","因此","三级","目标","由于","zset","READ","max","查询","来说",
              "Set","完成"]  # 需要删除的词语列表
Rs2 = []  # 建立存储分词的列表
for i in range(len(file_object2)):
    result = []
    seg_list = jieba.cut(file_object2[i])
    for w in seg_list:  # 读取每一行分词
        if len(w) >1:
            if w not in stop_words:
                result.append(w)
    Rs2.append(result)  # 将该行分词写入列表形式的总分词列表
# 写入CSV
file = open(r'D:\大三下\课程\项目实训\任务\16第16周\字节分词结果.csv', 'w',encoding='utf-8')
writer = csv.writer(file)  # 定义写入格式
writer.writerows(Rs2)  # 按行写入

word_freq = defaultdict(int)  # 使用defaultdict来初始化一个词频字典，初始值为0
# 统计词频
for row in Rs2:
    for word in row:
        word_freq[word] += 1
# 对词频字典按值进行排序
sorted_word_freq = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
# 打印前55个词频结果并写入CSV文件
with open(r'D:\大三下\课程\项目实训\任务\16第16周\字节词频统计结果.csv', 'w', encoding='utf-8', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Word', 'Frequency'])  # 写入表头
    for word, freq in sorted_word_freq[:30]:
        writer.writerow([word, freq])  # 写入每行数据
        print(word, freq)
# for word, freq in sorted_word_freq[:30]:
#     print(word, freq)
#获取前50个词频结果
top_words = sorted_word_freq[:30]
# text = ' '.join([' '.join(row) for row in Rs2])
shape = np.array(Image.open(r"D:\大三下\课程\项目实训\任务\16第16周\shape_cloud2.png"))
wordcloud = WordCloud(font_path=r'D:\大三下\课程\web数据管理\实验\实验三\实验三源代码\font.ttf',background_color='white', mask=shape,)
wordcloud.generate_from_frequencies(dict(top_words))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
wordcloud.to_file(r"D:\大三下\课程\项目实训\任务\16第16周\字节跳动\字节wordcloud30_yun.png")
# # #
file.close()