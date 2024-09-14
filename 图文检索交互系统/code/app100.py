import hashlib
import requests
from flask import Flask, jsonify, render_template, request, g, session
from utils import get_test_url, Log, User_Log, User_Log_txt, User_Log_img,User_Log_base
import client
import json
from trans import Translator
import datetime
app = Flask(__name__)
trans = Translator()
log = Log()
UserLog = User_Log()
UserLog_txt = User_Log_txt()
UserLog_img = User_Log_img()
User_Log_base = User_Log_base()
import random


# random.seed(999)
local_ip = 'http://192.168.3.65:5000'
server_ip = ''
app.secret_key = '123456'
# 这个时对照实验数据，存储在data2中。且只有3个三元组数据，需要替换真正实验数据
# with open('experiment.json', 'r') as j:
#     data2 = json.load(j)
with open('selected.json', 'r') as j:
    data2 = json.load(j)
# 可以在这里打开图文实验的数据，可以命名为data1,这里我依旧使用比较实验的数据进行占位
# with open('experiment.json', 'r') as j:
#     data1 = json.load(j)
with open('selected.json', 'r') as j:
    data1 = json.load(j)
@app.route('/')
def home():
    return render_template('home.html', local_ip=local_ip)


@app.route('/compare')
def compare():
    random_obj = data2[0]
    index = 1
    candidate_value = random_obj['candidate']
    target_value = random_obj['target']
    target_value = 'https://fashion-iq.oss-cn-beijing.aliyuncs.com/' + target_value + '.jpg'
    candidate_value = candidate_value + '.jpg'
    caption_value = random_obj['captions'][0] + '.' + random_obj['captions'][1]

    # caption_value = random.choice(random_obj['captions'])
    imgUrls = client.search_text_image(caption_value, candidate_value)
    print(imgUrls)
    candidate_value = 'https://fashion-iq.oss-cn-beijing.aliyuncs.com/' + candidate_value
    caption_value = trans.translate_2_zh(caption_value)

    print(caption_value)
    candidate_value_1 = imgUrls['result'][0]
    values = [target_value, candidate_value_1]
    target_random_value1 = random.choice(values)
    values.remove(target_random_value1)
    target_random_value2 = values[0]
    # log.add_triplet()
    return render_template('compare.html', index=index, candidate_value=candidate_value, caption_value=caption_value, target_random_value1=target_random_value1, target_random_value2=target_random_value2)


@app.route('/user_operation', methods=['POST'])
def handle_user_operation():
    # log.add_index()
    if request.method == 'POST':
        # 解析POST请求
        data = request.get_json()
        # 构造用户操作记录
        user_operation_record = {
            "user_currentTime":data["currentTime"],
            "description": data["caption_value"],
            "image_url": data["candidate_value"],
            "c5500_url": data["c5500_url"],
            "c5669_url": data["c5669_url"],
            "activeImage": data["activeImage"]
        }
        index = data["index"]
        print(index)
        print("当前获取数据:", user_operation_record)
        user_history = log.add_triplet(index,user_operation_record)
        index_num = int(index)
        log.save(index_num)
        print("用户操作历史",user_history)
        # 在后端输出

        # 这里要改成20，因为正式实验有20组实验gggggggggggggggg
        if index_num == 10:
            index_num = 0
            obj = data2[index_num]
        else:
            obj = data2[index_num]
        # print(obj)
        print("`````````````````````````",index_num)
        candidate_value = obj['candidate']
        target_value = obj['target']
        target_value = 'https://fashion-iq.oss-cn-beijing.aliyuncs.com/' + target_value + '.jpg'
        candidate_value = candidate_value + '.jpg'
        # caption_value = random.choice(obj['captions'])
        caption_value = obj['captions'][0] + '.' + obj['captions'][1]

        imgUrls = client.search_text_image(caption_value, candidate_value)
        # print(imgUrls)
        candidate_value = 'https://fashion-iq.oss-cn-beijing.aliyuncs.com/' + candidate_value
        caption_value = trans.translate_2_zh(caption_value)
        candidate_value_1 = imgUrls['result'][0]
        values = [target_value, candidate_value_1]
        target_random_value1 = random.choice(values)
        values.remove(target_random_value1)
        target_random_value2 = values[0]
        index = index_num + 1
        # 返回响应
        response_data = {
            "index": index,
            "candidate_value": candidate_value,
            "caption_value": caption_value,
            "target_random_value1": target_random_value1,
            "target_random_value2": target_random_value2
        }
        return jsonify(response_data)

@app.route('/last_experiment', methods=['POST'])
def last_experiment():
    if request.method == 'POST':
        # 解析POST请求
        data = request.get_json()
        index = int(data["index"])
        last_exp = log.get_triplet(index)
        index = index - 1
        # last_exp = user_history[index-1]
        print("上一组实验数据", last_exp)
        response_data = {
            "index": index,
            "image_url": last_exp["image_url"],
            "description": last_exp["description"],
            "c5500_url": last_exp["c5500_url"],
            "c5669_url": last_exp["c5669_url"],
            "activeImage": last_exp["activeImage"]
        }
        print(response_data)
        return jsonify(response_data)

# with open('static/initial.json', 'r') as f:
#     data1 = json.load(f)
index_user = 1
index_exp = 1
@app.route('/imgTxt')
def index0():
    global index_user
    global index_exp
    random_obj = data1[0]
    print(random_obj)
    target_value = random_obj['target']
    candidate_value = random_obj['candidate']
    caption_value = random.choice(random_obj['captions'])
    caption_value = trans.translate_2_zh(caption_value)

    now = datetime.datetime.now()  # 获取当前时间
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")  # 格式化时间为年月日小时分钟秒
    initial_value = {
        "start_time": current_time,
        "candidate": candidate_value + ".jpg",
        "text": caption_value,
        "target": target_value + ".jpg",
    }
    session["initial_value"] = initial_value
    # g.initial_value = initial_value
    print(initial_value)
    target_value = 'https://fashion-iq.oss-cn-beijing.aliyuncs.com/' + target_value + '.jpg'
    candidate_value = 'https://fashion-iq.oss-cn-beijing.aliyuncs.com/' + candidate_value + '.jpg'
    user_ID = index_user
    if index_user != 1:
        index_exp = 1
    index_user += 1
    user_search_round_log = session.get("search_log_None")
    return render_template('imgTxt.html',user_ID = user_ID, index_exp = index_exp, target_value=target_value, candidate_value=candidate_value, caption_value=caption_value)
index_user_img_txt = 1
index_exp_img_txt = 1
@app.route('/imgTxt2')
def index1():
    global index_user_img_txt
    global index_exp_img_txt
    random_obj = data1[0]
    print(random_obj)
    target_value = random_obj['target']
    candidate_value = random_obj['candidate']
    caption_value = random.choice(random_obj['captions'])
    caption_value = trans.translate_2_zh(caption_value)
    now = datetime.datetime.now()  # 获取当前时间
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")  # 格式化时间为年月日小时分钟秒
    initial_value = {
        "start_time": current_time,
        "candidate": candidate_value + ".jpg",
        "text": caption_value,
        "target": target_value + ".jpg",
    }
    session["initial_value"] = initial_value
    # g.initial_value = initial_value
    print(initial_value)
    target_value = 'https://fashion-iq.oss-cn-beijing.aliyuncs.com/' + target_value + '.jpg'
    candidate_value = 'https://fashion-iq.oss-cn-beijing.aliyuncs.com/' + candidate_value + '.jpg'
    user_ID = index_user_img_txt
    if index_user_img_txt != 1:
        index_exp_img_txt = 1
    index_user_img_txt += 1
    user_search_round_log = session.get("search_log_None")
    return render_template('imgTxt2.html',user_ID = user_ID, index_exp = index_exp_img_txt, target_value=target_value, candidate_value=candidate_value, caption_value=caption_value)
index_user_img = 1
index_exp_img = 1
@app.route('/img')
def index2():
    global index_user_img
    global index_exp_img
    random_obj = data1[0]
    target_value = random_obj['target']
    candidate_value = random_obj['candidate']
    now = datetime.datetime.now()  # 获取当前时间
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")  # 格式化时间为年月日小时分钟秒
    initial_value_img = {
        "start_time": current_time,
        "candidate": candidate_value + ".jpg",
        "target": target_value + ".jpg",
    }
    session["initial_value_img"] = initial_value_img
    target_value = 'https://fashion-iq.oss-cn-beijing.aliyuncs.com/' + target_value + '.jpg'
    candidate_value = 'https://fashion-iq.oss-cn-beijing.aliyuncs.com/' + candidate_value + '.jpg'
    user_ID = index_user_img
    if index_user_img != 1:
        index_exp_img = 1
    index_user_img += 1
    user_search_round_log_img = session.get("search_log_None")
    return render_template('image.html', user_ID_img=user_ID, index_exp_img=index_exp_img, target_value=target_value, candidate_value=candidate_value)
user_id_txt = 1
index_exp_txt =1

@app.route('/txt')
def index3():
    global user_id_txt
    global index_exp_txt
    random_obj = data1[0]
    target_value = random_obj['target']
    caption_value = random.choice(random_obj['captions'])
    caption_value = trans.translate_2_zh(caption_value)
    now = datetime.datetime.now()  # 获取当前时间
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")  # 格式化时间为年月日小时分钟秒
    initial_value = {
        "start_time": current_time,
        "text": caption_value,
        "target": target_value + ".jpg",
    }
    session["initial_value_txt"] = initial_value
    target_value = 'https://fashion-iq.oss-cn-beijing.aliyuncs.com/' + target_value + '.jpg'
    user_ID_txt = user_id_txt
    if user_id_txt != 1:
        index_exp_txt = 1
    user_id_txt += 1
    user_search_round_log_txt = session.get("search_log_None")
    return render_template('txt.html', user_ID_txt=user_ID_txt, index_exp_txt=index_exp_txt, target_value=target_value, caption_value=caption_value)

@app.route("/searchT", methods=["POST"])
def searchT():
    global round_num_txt
    data = request.json
    searchText = data["searchText"]
    print("搜索文本：", searchText)
    searchText1 = trans.translate_2_en(searchText)
    # print(searchText1)
    imgUrls = client.search_text(searchText1)
    search_result_txt = [item[47:] for item in imgUrls['result']]
    print(imgUrls)
    print(search_result_txt)
    now = datetime.datetime.now()  # 获取当前时间
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")  # 格式化时间为年月日小时分钟秒
    search_round_value_txt = {
        "text": searchText,
        "search_time": current_time,
        "result": search_result_txt,
    }
    user_search_round_log_txt = UserLog_txt.add_triplet(round_num_txt, search_round_value_txt)
    session["search_round_value_txt"] = user_search_round_log_txt
    print(user_search_round_log_txt)
    user_search_round_log_txt = session.get("search_log_None")
    print(user_search_round_log_txt)
    round_num_txt += 1
    return jsonify({"imgUrls": imgUrls, "round_num_txt": round_num_txt - 1})


@app.route("/searchI", methods=["POST"])
def searchI():
    # 获取搜索文本和参考图片的URL
    global round_num_img
    data = request.json
    refImageUrl = data["refImageUrl"]
    print("参考图片URL：", refImageUrl)
    refImageUrl = refImageUrl[47:]
    print(refImageUrl)
    imgUrls = client.search_image( refImageUrl)
    search_result = [item[47:] for item in imgUrls['result']]
    print(imgUrls)
    print(search_result)
    now = datetime.datetime.now()  # 获取当前时间
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")  # 格式化时间为年月日小时分钟秒
    search_round_value_img = {
        "candidate": refImageUrl,
        "search_time": current_time,
        "result": search_result,
    }
    user_search_round_log_img = UserLog.add_triplet(round_num_img, search_round_value_img)
    session["search_round_value_img"] = user_search_round_log_img
    print(user_search_round_log_img)
    user_search_round_log_img = session.get("search_log_None")
    print(user_search_round_log_img)
    round_num_img += 1
    return jsonify({"imgUrls": imgUrls, "round_num_img": round_num_img - 1})


round_num = 1
@app.route("/searchIT", methods=["POST"])
def searchIT():
    # 获取搜索文本和参考图片的URL
    global round_num
    data = request.json
    searchText = data["searchText"]
    refImageUrl = data["refImageUrl"]
    print("搜索文本：", searchText)
    print("参考图片URL：", refImageUrl)
    refImageUrl = refImageUrl[47:]
    print(refImageUrl)
    searchText1 = trans.translate_2_en(searchText)
    print(searchText1)
    imgUrls = client.search_text_image(searchText1,refImageUrl)
    search_result = [item[47:] for item in imgUrls['result']]
    print(imgUrls)
    print(search_result)
    now = datetime.datetime.now()  # 获取当前时间
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")  # 格式化时间为年月日小时分钟秒
    search_round_value = {
        "text":searchText,
        "candidate":refImageUrl,
        "search_time":current_time,
        "result":search_result,
    }
    user_search_round_log = UserLog.add_triplet(round_num,search_round_value)
    session["search_round_value"] = user_search_round_log
    print(user_search_round_log)
    user_search_round_log = session.get("search_log_None")
    print(user_search_round_log)
    round_num += 1
    return jsonify({"imgUrls": imgUrls, "round_num": round_num-1})


@app.route("/searchIT2", methods=["POST"])
def searchIT2():
    # 获取搜索文本和参考图片的URL
    global round_num
    data = request.json
    searchText = data["searchText"]
    refImageUrl = data["refImageUrl"]
    print("搜索文本：", searchText)
    print("参考图片URL：", refImageUrl)
    refImageUrl = refImageUrl[47:]
    print(refImageUrl)
    searchText1 = trans.translate_2_en(searchText)
    print(searchText1)
    # 随机替换8张图片
    # refImageUrl= "245600258X.jpg"
    imgUrls = client.search_text_image2(searchText1,refImageUrl)
    search_result = [item[47:] for item in imgUrls['result']]
    print(imgUrls)
    print(search_result)
    now = datetime.datetime.now()  # 获取当前时间
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")  # 格式化时间为年月日小时分钟秒
    search_round_value = {
        "text":searchText,
        "candidate":refImageUrl,
        "search_time":current_time,
        "result":search_result,
    }
    user_search_round_log = UserLog.add_triplet(round_num,search_round_value)
    session["search_round_value"] = user_search_round_log
    print(user_search_round_log)
    user_search_round_log = session.get("search_log_None")
    print(user_search_round_log)
    round_num += 1
    return jsonify({"imgUrls": imgUrls, "round_num": round_num-1})

@app.route("/matchIT2", methods=["POST"])
def matchIT2():
    global index_exp_img_txt
    global index_user_img_txt
    global round_num
    data = request.get_json()
    candidate_success = data.get("candidate_success")[47:]
    reference_Image = data["reference_Image"][47:]
    search_text = data["search_text"]
    now = datetime.datetime.now()  # 获取当前时间
    success_time = now.strftime("%Y-%m-%d %H:%M:%S")  # 格式化时间为年月日小时分钟秒
    success_exp = {
        "reference_Image": reference_Image,
        "candidate_success": candidate_success,
        "search_text": search_text,
        "success_time": success_time,
    }
    initial_data = session.get("initial_value")
    # print("initial值:", initial_data)
    search_log = session.get("search_round_value")
    # print("search_log值:", search_log)
    User_Log_base.save_baseModel(index_user_img_txt-1,index_exp_img_txt,initial_data,search_log,success_exp)
    print(success_exp)
    index_exp_img_txt += 1
    # 333333333333333333333333gggggggggggggggggggg
    if index_exp_img_txt == 101:
        index_exp_img_txt = 0
        random_obj = data1[index_exp_img_txt]
        index_exp_img_txt = 1
    else:
        random_obj = data2[index_exp_img_txt-1]
    # random_obj = random.choice(data1
    # random_obj = data1[index_exp-1]
    target_value_org = random_obj['target']
    candidate_value_org = random_obj['candidate']
    caption_value = random.choice(random_obj['captions'])
    target_value = 'https://fashion-iq.oss-cn-beijing.aliyuncs.com/' + target_value_org + '.jpg'
    candidate_value = 'https://fashion-iq.oss-cn-beijing.aliyuncs.com/' + candidate_value_org + '.jpg'
    caption_value = trans.translate_2_zh(caption_value)
    round_num = 1
    response_data = {
        "round_num":round_num,
        "index_exp":index_exp_img_txt,
        "target_value":target_value,
        "candidate_value":candidate_value,
        "caption_value":caption_value,
    }
    print(response_data)
    session["search_log_None"] = {}
    session["initial_value"] = {
        "candidate": candidate_value_org,
        "satrt_time": success_time,
        "target": target_value_org,
        "text": caption_value
    }
    return jsonify(response_data)

@app.route("/Next_exp2", methods=["POST"])
def Next_exp2():
    global index_user_img_txt
    global round_num
    global index_exp_img_txt
    if round_num <= 2:
        return_value = None
    else:
        index_exp_img_txt += 1
        # random_obj = random.choice(data1)

        # 此处需要把4改为16
        if index_exp_img_txt == 100:
            index_exp_img_txt = 0
            random_obj = data1[index_exp_img_txt]
            index_exp_img_txt = 1
        else:
            random_obj = data1[index_exp_img_txt - 1]
        # random_obj = data1[index_exp - 1]
        target_value = random_obj['target']
        candidate_value = random_obj['candidate']
        caption_value = random.choice(random_obj['captions'])
        target_value = 'https://fashion-iq.oss-cn-beijing.aliyuncs.com/' + target_value + '.jpg'
        candidate_value = 'https://fashion-iq.oss-cn-beijing.aliyuncs.com/' + candidate_value + '.jpg'
        caption_value = trans.translate_2_zh(caption_value)
        round_num = 1
        response_data = {
            "round_num": round_num,
            "index_exp": index_exp_img_txt,
            "target_value": target_value,
            "candidate_value": candidate_value,
            "caption_value": caption_value,
        }
        return_value = response_data
        data = request.get_json()
        targetImage_fail = data.get("target_Image")[47:]
        referenceImage_fail = data["reference_Image"][47:]
        search_text = data["search_text"]
        now = datetime.datetime.now()  # 获取当前时间
        fail_time = now.strftime("%Y-%m-%d %H:%M:%S")  # 格式化时间为年月日小时分钟秒
        fail_exp = {
            "referenceImage_fail": referenceImage_fail,
            "targetImage_fail": targetImage_fail,
            "search_text": search_text,
            "fail_time": fail_time,
        }
        initial_data = session.get("initial_value")
        # print("initial值:", initial_data)
        search_log = session.get("search_round_value")
        # print("search_log值:", search_log)
        User_Log_base.save_baseModel(index_user_img_txt - 1, index_exp_img_txt-1, initial_data, search_log, fail_exp)
        print(fail_exp)
    return return_value

@app.route("/matchIT", methods=["POST"])
def matchIT():
    global index_exp
    global index_user
    global round_num
    data = request.get_json()
    candidate_success = data.get("candidate_success")[47:]
    reference_Image = data["reference_Image"][47:]
    search_text = data["search_text"]
    now = datetime.datetime.now()  # 获取当前时间
    success_time = now.strftime("%Y-%m-%d %H:%M:%S")  # 格式化时间为年月日小时分钟秒
    success_exp = {
        "reference_Image": reference_Image,
        "candidate_success": candidate_success,
        "search_text": search_text,
        "success_time": success_time,
    }
    initial_data = session.get("initial_value")
    # print("initial值:", initial_data)
    search_log = session.get("search_round_value")
    # print("search_log值:", search_log)
    UserLog.save(index_user-1,index_exp,initial_data,search_log,success_exp)
    print(success_exp)
    index_exp += 1
    # ggggggggggggggggggggggggggggggggggggggggggg
    if index_exp == 11:
        index_exp = 0
        random_obj = data1[index_exp]
        index_exp = 1
    else:
        random_obj = data2[index_exp-1]
    # random_obj = random.choice(data1
    # random_obj = data1[index_exp-1]
    target_value_org = random_obj['target']
    candidate_value_org = random_obj['candidate']
    caption_value = random.choice(random_obj['captions'])
    target_value = 'https://fashion-iq.oss-cn-beijing.aliyuncs.com/' + target_value_org + '.jpg'
    candidate_value = 'https://fashion-iq.oss-cn-beijing.aliyuncs.com/' + candidate_value_org + '.jpg'
    caption_value = trans.translate_2_zh(caption_value)
    round_num = 1
    response_data = {
        "round_num":round_num,
        "index_exp":index_exp,
        "target_value":target_value,
        "candidate_value":candidate_value,
        "caption_value":caption_value,
    }
    print(response_data)
    session["search_log_None"] = {}
    session["initial_value"] = {
        "candidate": candidate_value_org,
        "satrt_time": success_time,
        "target": target_value_org,
        "text": caption_value
    }
    return jsonify(response_data)
round_num_txt = 1
@app.route("/matchT", methods=["POST"])

def matchT():
    global index_exp_txt
    global user_id_txt
    global round_num_txt
    data = request.get_json()
    candidate_success = data.get("candidate_success")[47:]
    target_Image = data["target_Image"][47:]
    search_text = data["search_text"]
    now = datetime.datetime.now()  # 获取当前时间
    success_time = now.strftime("%Y-%m-%d %H:%M:%S")  # 格式化时间为年月日小时分钟秒
    success_exp_txt = {
        "target_Image": target_Image,
        "candidate_success": candidate_success,
        "search_text": search_text,
        "success_time": success_time,
    }
    initial_data_txt = session.get("initial_value_txt")
    print("initial值:", initial_data_txt)
    search_log_txt = session.get("search_round_value_txt")
    print("search_log值:", search_log_txt)
    UserLog_txt.save(user_id_txt-1,index_exp_txt,initial_data_txt,search_log_txt,success_exp_txt)
    print(success_exp_txt)
    index_exp_txt += 1
    # random_obj = random.choice(data1)
    if index_exp_txt == 11:
        index_exp_txt = 0
        random_obj = data1[index_exp_txt]
        index_exp_txt = 1
    else:
        random_obj = data1[index_exp_txt-1]
    # random_obj = data1[index_exp_txt-1]
    print(random_obj)
    target_value_org = random_obj['target']
    caption_value = random.choice(random_obj['captions'])
    target_value = 'https://fashion-iq.oss-cn-beijing.aliyuncs.com/' + target_value_org + '.jpg'
    caption_value = trans.translate_2_zh(caption_value)
    round_num_txt = 1
    response_data = {
        "round_num_txt":round_num_txt,
        "index_exp_txt":index_exp_txt,
        "target_value":target_value,
        "caption_value":caption_value,
    }
    print(response_data)
    session["search_log_None"] = {}
    session["initial_value_txt"] = {
        "satrt_time": success_time,
        "target": target_value_org,
        "text": caption_value
    }
    return jsonify(response_data)
round_num_img = 1

@app.route("/matchI", methods=["POST"])
def matchI():
    global index_exp_img
    global index_user_img
    global round_num_img
    data = request.get_json()
    candidate_success = data.get("candidate_success")[47:]
    reference_Image = data["reference_Image"][47:]
    now = datetime.datetime.now()  # 获取当前时间
    success_time = now.strftime("%Y-%m-%d %H:%M:%S")  # 格式化时间为年月日小时分钟秒
    success_exp_img = {
        "reference_Image": reference_Image,
        "candidate_success": candidate_success,
        "success_time": success_time,
    }
    initial_data_img = session.get("initial_value_img")
    search_log_img = session.get("search_round_value_img")
    UserLog_img.save(index_user_img-1,index_exp_img,initial_data_img,search_log_img,success_exp_img)
    index_exp_img += 1
    # 此处正式实验时应该改为16
    if index_exp_img == 11:
        index_exp_img = 0
        random_obj = data1[index_exp_img]
        index_exp_img = 1
    else:
        random_obj = data1[index_exp_img-1]
    # random_obj = random.choice(data1)
    # random_obj = data1[index_exp_img - 1]
    target_value_org = random_obj['target']
    candidate_value_org = random_obj['candidate']
    target_value = 'https://fashion-iq.oss-cn-beijing.aliyuncs.com/' + target_value_org + '.jpg'
    candidate_value = 'https://fashion-iq.oss-cn-beijing.aliyuncs.com/' + candidate_value_org + '.jpg'
    round_num_img = 1
    response_data = {
        "round_num_img":round_num_img,
        "index_exp_img":index_exp_img,
        "target_value":target_value,
        "candidate_value":candidate_value,
    }
    print(response_data)
    session["search_log_None"] = {}
    session["initial_value_img"] = {
        "candidate": candidate_value_org,
        "satrt_time": success_time,
        "target": target_value_org,
    }
    return jsonify(response_data)

@app.route("/Next_exp", methods=["POST"])
def Next_exp():
    global index_user
    global round_num
    global index_exp
    if round_num <= 2:
        return_value = None
    else:
        index_exp += 1
        # random_obj = random.choice(data1)

        # 此处需要把4改为16
        if index_exp == 11:
            index_exp = 0
            random_obj = data1[index_exp]
            index_exp = 1
        else:
            random_obj = data1[index_exp - 1]
        target_value = random_obj['target']
        candidate_value = random_obj['candidate']
        caption_value = random.choice(random_obj['captions'])
        target_value = 'https://fashion-iq.oss-cn-beijing.aliyuncs.com/' + target_value + '.jpg'
        candidate_value = 'https://fashion-iq.oss-cn-beijing.aliyuncs.com/' + candidate_value + '.jpg'
        caption_value = trans.translate_2_zh(caption_value)
        round_num = 1
        response_data = {
            "round_num": round_num,
            "index_exp": index_exp,
            "target_value": target_value,
            "candidate_value": candidate_value,
            "caption_value": caption_value,
        }
        return_value = response_data
        data = request.get_json()
        targetImage_fail = data.get("target_Image")[47:]
        referenceImage_fail = data["reference_Image"][47:]
        search_text = data["search_text"]
        now = datetime.datetime.now()  # 获取当前时间
        fail_time = now.strftime("%Y-%m-%d %H:%M:%S")  # 格式化时间为年月日小时分钟秒
        fail_exp = {
            "referenceImage_fail": referenceImage_fail,
            "targetImage_fail": targetImage_fail,
            "search_text": search_text,
            "fail_time": fail_time,
        }
        initial_data = session.get("initial_value")
        # print("initial值:", initial_data)
        search_log = session.get("search_round_value")
        # print("search_log值:", search_log)
        UserLog.save(index_user - 1, index_exp-1, initial_data, search_log, fail_exp)
        print(fail_exp)
    return return_value

@app.route("/Next_exp_txt", methods=["POST"])
def Next_exp_txt():
    global user_id_txt
    global round_num_txt
    global index_exp_txt
    if round_num_txt <= 2:
        return_value = None
    else:
        index_exp_txt += 1
        # ggggggggggggggggggggggggg
        if index_exp_txt == 11:
            index_exp_txt = 0
            random_obj = data1[index_exp_txt]
            index_exp_txt = 1
        else:
            random_obj = data1[index_exp_txt - 1]
        # random_obj = random.choice(data1)
        # random_obj = data1[index_exp_txt - 1]
        target_value = random_obj['target']
        caption_value = random.choice(random_obj['captions'])
        target_value = 'https://fashion-iq.oss-cn-beijing.aliyuncs.com/' + target_value + '.jpg'
        caption_value = trans.translate_2_zh(caption_value)
        round_num_txt = 1
        response_data = {
            "round_num_txt": round_num_txt,
            "index_exp_txt": index_exp_txt,
            "target_value": target_value,
            "caption_value": caption_value,
        }
        return_value = response_data
        data = request.get_json()
        targetImage_fail = data.get("target_Image")[47:]
        search_text = data["search_text"]
        now = datetime.datetime.now()  # 获取当前时间
        fail_time = now.strftime("%Y-%m-%d %H:%M:%S")  # 格式化时间为年月日小时分钟秒
        fail_exp_txt = {
            "targetImage_fail": targetImage_fail,
            "search_text": search_text,
            "fail_time": fail_time,
        }
        initial_data_txt = session.get("initial_value_txt")
        # print("initial值:", initial_data)
        search_log_txt = session.get("search_round_value_txt")
        # print("search_log值:", search_log)
        # UserLog.save(index_user - 1, index_exp-1, initial_data_txt, search_log_txt, fail_exp_txt)
        UserLog_txt.save(index_user, index_exp, initial_data_txt, search_log_txt, fail_exp_txt)
        print(fail_exp_txt)
    return return_value

@app.route("/Next_exp_img", methods=["POST"])
def Next_exp_img():
    global index_user_img
    global round_num_img
    global index_exp_img
    if round_num_img <= 2:
        return_value = None
    else:
        index_exp_img += 1
        if index_exp_img == 11:
            index_exp_img = 0
            random_obj = data1[index_exp_img]
            index_exp_img = 1
        else:
            random_obj = data1[index_exp_img - 1]
        # random_obj = random.choice(data1)
        # random_obj = data1[index_exp_img - 1]
        target_value = random_obj['target']
        candidate_value = random_obj['candidate']
        target_value = 'https://fashion-iq.oss-cn-beijing.aliyuncs.com/' + target_value + '.jpg'
        candidate_value = 'https://fashion-iq.oss-cn-beijing.aliyuncs.com/' + candidate_value + '.jpg'
        round_num_img = 1
        response_data = {
            "round_num_img": round_num_img,
            "index_exp_img": index_exp_img,
            "target_value": target_value,
            "candidate_value": candidate_value,
        }
        return_value = response_data
        data = request.get_json()
        targetImage_fail = data.get("target_Image")[47:]
        referenceImage_fail = data["reference_Image"][47:]
        now = datetime.datetime.now()  # 获取当前时间
        fail_time = now.strftime("%Y-%m-%d %H:%M:%S")  # 格式化时间为年月日小时分钟秒
        fail_exp_img = {
            "referenceImage_fail_img": referenceImage_fail,
            "targetImage_fail_img": targetImage_fail,
            "fail_time_img": fail_time,
        }
        initial_data_img = session.get("initial_value_img")
        # print("initial值:", initial_data)
        search_log_img = session.get("search_round_value_img")
        # print("search_log值:", search_log)
        UserLog_img.save(index_user_img - 1, index_exp_img-1, initial_data_img, search_log_img, fail_exp_img)
    return return_value

@app.route('/withdraw', methods=['POST'])
def index():
    try:
        # 实现“撤回”按钮的业务逻辑
        # ...
        # images = ['1.jpg', '245600258X.jpg', '978980539X.jpg', '978981366X.jpg']
        # images = "https://th.bing.com/th/id/OIP.uZ319ApnRKIJnflISWnOOAHaE_?pid=ImgDet&rs=1"
        images = "https://fashion-iq.oss-cn-beijing.aliyuncs.com/B008U0LKJ2.jpg"
        # 返回包含respone JSON信息的Response对象，成功200
        result = {
            # 'image': random.choice(images)  # 随机返回一张图片
            'image':images  # 随机返回一张图片
        }
        # response_data = {"image": "245600258X.jpg"}
        status_code = 200
        resp =  jsonify(result)
        # resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp, status_code
    except Exception as e:
        # 返回错误信息
        return str(e), 500

@app.route('/txt2img')
def hello_world():
    print()
    return render_template('txt2img.html', url_init=get_test_url(2))


@app.route('/img2img')
def img2img():
    return render_template('img2img.html', url_init=get_test_url(1))

@app.route('/imgtxt2img')
def imgtxt2img():
    return render_template('imgtxt2img.html', url_init=get_test_url(2))

# TXT 2 IMG BLOCK
# 点击刷新按钮
@app.route('/txt2img/refresh')
def refresh_TI():  # put application's code here
    # 前端的reference图片进行刷新
    text = '收到 文本-->图片 前端的REFRESH指令'

    image = get_test_url(2)
    return jsonify(image)


# 点击检索按钮
@app.route('/txt2img/search')
def send_TI():  # put application's code here
    # 处理前端的 文本-->图片 的检索指令
    text = '收到 文本-->图片 前端的SEARCH指令'

    img_src = request.args.get('imgSrc')
    search_text = request.args.get('searchText')
    print('收到前端图片：', img_src)
    print('收到前端搜索文本：', search_text)
    # 进行图片搜索并得到图片地址列表

    image_urls = get_test_url(9)
    return jsonify(image_urls) #前端收到，进行展示




# IMG2IMG
# 点击刷新按钮
@app.route('/img2img/refresh')
def refresh_II():
    text = '收到 图片-->图片 前端的REFRESH指令'
    print(text)

    image = get_test_url(1)
    return jsonify(image)


# 点击检索按钮
@app.route('/img2img/search')
def send_II():  # put application's code here
    # 处理前端的 图片-->图片 的检索指令
    text = '收到 图片-->图片 前端的SEARCH指令'

    img_src = request.args.get('imgSrc')
    print('收到前端图片：', img_src)
    # 进行图片搜索并得到图片地址列表
    image_urls = get_test_url(9)
    return jsonify(image_urls) #前端收到，进行展示





# IMGTXT2IMG

# 点击刷新按钮
@app.route('/imgtxt2img/refresh')
def refresh_ITI():
    text = '收到 图片+文本-->图片 前端的REFRESH指令'
    print(text)
    image = get_test_url(2)
    return jsonify(image)

# 点击检索按钮
@app.route('/imgtxt2img/search')
def search_ITI():  # put application's code here
    # 处理前端的 图片-->图片 的检索指令
    text = '收到 图片+文本-->图片 前端的SEND指令'
    print(text)

    img_src = request.args.get('imgSrc')
    search_text = request.args.get('searchText')
    print('收到前端图片：', img_src)
    print('收到前端搜索文本：', search_text)
    # 进行图片搜索并得到图片地址列表

    image_urls = get_test_url(9)
    return jsonify(image_urls) #前端收到，进行展示

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080, debug=True)
if __name__ == '__main__':
    app.run(port='8082')
# --host=0.0.0.0 --port=8080

# http://10.200.95.46:8080/txt2img/refresh
# http://10.200.95.46:8080/txt2img/send