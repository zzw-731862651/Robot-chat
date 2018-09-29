from aip import AipSpeech
from aip import AipNlp
import os
import tuling
from uuid import uuid4

#注意：ffmpeg,目前音乐领域最牛逼的转换音频视频的软件工具，转换音频格式
# 备注：连接之前，先要在cmd中输入mongod --dbpath f:\data\db，打开一个应用程序，然后在另外打开一个cmd,输入mongo,启动芒果数据库；才可以使用
#注意：这个运行环境是python3.6


APP_ID = '11793791'
API_KEY = 'iaTErc4r5GXNT56tYnlVtVtk'
SECRET_KEY = '24P7ImcU7kEaOmoBxDy9giNe6evkYca4'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)     #将语音识别成汉字的实例
nlp_client = AipNlp(APP_ID, API_KEY, SECRET_KEY)        #将汉字转换成语音

# # 读取文件
# filePath = "wyn.m4a"
#
#
def get_file_content(filePath):    #文件格式转换
    os.system(f"ffmpeg -y -i {filePath}  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 {filePath}.pcm")   #环境python3.6.这句命令很重要，转变文件格式
    with open(f"{filePath}.pcm", 'rb') as fp:
        return fp.read()

def audio2text(file_name):
    # *************************连接mongodb数据库*******************************************
    # 备注：连接之前，先要在cmd中输入mongod --dbpath f:\data\db，打开一个应用程序，然后在另外打开一个cmd,输入mongo,启动芒果数据库；才可以使用
    import pymongo
    from bson import ObjectId
    mclient = pymongo.MongoClient(host="127.0.0.1", port=27017)
    mongo_db = mclient["zhao"]
    # ******************************************************************************************
    # 识别本地文件
    liu = get_file_content(file_name)
    # print('2333',liu)  #这里是bytes流
    res = client.asr(liu, 'pcm', 16000, {
        'dev_pid': 1536,
    })
    # print('3434',res)   #{'corpus_no': '6600319898580623958', 'err_msg': 'success.', 'err_no': 0, 'result': ['谢飞机帅吗'], 'sn': '151915580131536756730'}
    if res.get("result"):
        b = res.get("result")[0]
        mongo_db.record.insert_one({"提问":b})
        print('****',res.get("result")[0])      #获取到语音识别的汉字结果
    else:
        print(res)   #没有获取到结果
    q = res.get("result")[0]
    # res = mongo_db.record.find()
    # for i in res:
    #     print('这是mongodb的提问数据：', i)
    return q
#
# # q = res.get("result")[0]    #这里是获取到上面的wyn.m4a的语音识别后的汉字，然后下面的代码可以根据语音识别的结果汉字作为参考匹配，做出智能回复
# # q = "你吃早饭了吗"    #这个q可以是上面的语音识别的结果，然后下面的代码根据语音识别的结果，做出智能回复
# # q = "你今天过的怎么样"     #下面的代码拿a和q进行比较，然后根据智能代码，做出相应的回应。并打开播放器播放出来
# q = "你初中班主任的名字叫什么"     #下面的代码拿a和q进行比较，然后根据智能代码，做出相应的回应。并打开播放器播放出来
# a = "我不知道你在说什么"
#
# if nlp_client.simnet(q, "你的名字叫什么").get("score") >= 0.7:     #做两个字符串的相似度比较，然后a是回答
#     a = "我叫赵振伟"
#
# if nlp_client.simnet(q, "你今年几岁了").get("score") >= 0.7:   #做两个字符串的相似度比较，然后a是回答
#     a = "我今年27岁了"
#
# if nlp_client.simnet(q, "你吃饭了吗").get("score") >= 0.7:   #做两个字符串的相似度比较，然后a是回答
#     a = "刚吃过，你呢"
#
#
# if nlp_client.simnet(q, "你今天过的好吗").get("score") >= 0.7:   #做两个字符串的相似度比较，然后a是回答
#     a = "很好，学了一天的知识，很充实，谢谢您的关心"
#
# if nlp_client.simnet(q, "你初中班主任老师的名字叫什么").get("score") >= 0.7:   #做两个字符串的相似度比较，然后a是回答
#     a = "张蔚"
#

def text2audio(text):

    file_name = f"{uuid4()}.wav"   #动态修改文件名，清除缓存问题
    result = client.synthesis(text, 'zh', 1, {
        "spd": 4,    #语速，取值0-9，默认为5中语速
        'vol': 7,   #音量，取值0-15，默认为5中音量
        "pit": 8,   #音调，取值0-9，默认为5中语调
        "per": 4    #发音人选择, 0为女声，1为男声，3为情感合成-度逍遥，4为情感合成-度丫丫，默认为普通女
    })

    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        with open(file_name, 'wb') as f:
            f.write(result)


    # os.system("auido.mp3")
    return file_name


def my_nlp(q,uid):
    # *************************连接mongodb数据库*******************************************
    #备注：连接之前，先要在cmd中输入mongod --dbpath f:\data\db，打开一个应用程序，然后在另外打开一个cmd,输入mongo,启动芒果数据库；才可以使用
    import pymongo
    from bson import ObjectId
    mclient = pymongo.MongoClient(host="127.0.0.1", port=27017)
    mongo_db = mclient["zhao"]
    # ******************************************************************************************
    a = "我不知道你在说什么"

    # if nlp_client.simnet(q, "你的名字叫什么").get("score") >= 0.7:  # 做两个字符串的相似度比较，然后a是回答
    #     a = "我叫赵振伟"
    #     return a

    if nlp_client.simnet(q, "你今年几岁了").get("score") >= 0.7:  # 做两个字符串的相似度比较，然后a是回答
        a = "我今年27岁了"
        return a

    if nlp_client.simnet(q, "你吃饭了吗").get("score") >= 0.7:  # 做两个字符串的相似度比较，然后a是回答
        a = "刚吃过，你呢"
        return a

    if nlp_client.simnet(q, "你今天过的好吗").get("score") >= 0.7:  # 做两个字符串的相似度比较，然后a是回答
        a = "很好，学了一天的知识，很充实，谢谢您的关心"
        return a

    if nlp_client.simnet(q, "你初中班主任老师的名字叫什么").get("score") >= 0.7:  # 做两个字符串的相似度比较，然后a是回答
        a = "张蔚"
        return a

    a = tuling.to_tuling(q,uid)
    mongo_db.record.insert_one({"回答": a})
    print('--->',a)   #图灵机器人返回的回答，汉字。
    res = mongo_db.record.find()
    for i in res:
        print('这是mongodb的回答数据：',i)
    return a








