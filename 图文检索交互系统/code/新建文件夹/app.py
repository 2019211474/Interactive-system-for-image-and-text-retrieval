import hashlib
import requests
from flask import Flask, jsonify, render_template, request, g
from utils import get_test_url, Log, User_Log
import client
import json
from trans import Translator
import datetime
import random
# with open('static/initial.json','r') as f:
#     data = json.load(f)
# random_obj = random.choice(data)
# target_value = random_obj['target']
# candidate_value = random_obj['candidate']
# caption_value = random_obj['captions']
# target_value = 'https://fashion-iq.oss-cn-beijing.aliyuncs.com/' + target_value + '.jpg'
# candidate_value = 'https://fashion-iq.oss-cn-beijing.aliyuncs.com/' + candidate_value + '.jpg'
# print(target_value)
# print(random_obj)
# print(caption_value)
# from flask_cors import CORS
app = Flask(__name__)
trans = Translator()
log = Log()
UserLog = User_Log()
# CORS(app)
import random


@app.route('/')
def home():
    return render_template('home.html')
    # return "Hello, World!"
    # return render_template('compare.html')
    # return render_template('imgTxt.html')

# @app.route('/compare')
# def compare():
#     with open('static/initial.json', 'r') as j:
#         data = json.load(j)
#     random_obj = random.choice(data)
#     candidate_value = random_obj['candidate']
#     caption_value = random.choice(random_obj['captions'])
#     candidate_value = 'https://fashion-iq.oss-cn-beijing.aliyuncs.com/' + candidate_value + '.jpg'
#     return render_template('compare.html', candidate_value=candidate_value, caption_value=caption_value)

with open('experiment.json', 'r') as j:
    data2 = json.load(j)
@app.route('/compare')
def compare():
    random_obj = data2[0]
    index = 1
    candidate_value = random_obj['candidate']
    target_value = random_obj['target']
    target_value = 'https://fashion-iq.oss-cn-beijing.aliyuncs.com/' + target_value + '.jpg'
    candidate_value = candidate_value + '.jpg'
    caption_value = random.choice(random_obj['captions'])
    imgUrls = client.search_text_image(caption_value, candidate_value)
    print(imgUrls)
    candidate_value = 'https://fashion-iq.oss-cn-beijing.aliyuncs.com/' + candidate_value
    caption_value = trans.translate_2_zh(caption_value)
    candidate_value_1 = imgUrls['result'][0]
    values = [target_value, candidate_value_1]
    target_random_value1 = random.choice(values)
    values.remove(target_random_value1)
    target_random_value2 = values[0]

    # log.add_triplet()

    return render_template('compare.html', index=index, candidate_value=candidate_value, caption_value=caption_value, target_random_value1=target_random_value1, target_random_value2=target_random_value2)

with open('experiment.json', 'r') as j:
    data3 = json.load(j)
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

        if index_num == 3:
            index_num = 0
            obj = data3[index_num]
        else:
            obj = data3[index_num]
        # print(obj)
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

with open('static/initial.json', 'r') as f:
    data1 = json.load(f)

index_user = 1
index_exp = 1
@app.route('/imgTxt')
def index0():
    global index_user
    global index_exp
    random_obj = random.choice(data1)
    target_value = random_obj['target']
    candidate_value = random_obj['candidate']
    caption_value = random.choice(random_obj['captions'])
    caption_value = trans.translate_2_zh(caption_value)
    now = datetime.datetime.now()  # 获取当前时间
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")  # 格式化时间为年月日小时分钟秒
    initial_value = {
        "start_time": current_time,
        "candidate": candidate_value + ".Jpg",
        "text": caption_value,
        "target": target_value + ".Jpg",
    }
    g.initial_value = initial_value
    print(initial_value)
    target_value = 'https://fashion-iq.oss-cn-beijing.aliyuncs.com/' + target_value + '.jpg'
    candidate_value = 'https://fashion-iq.oss-cn-beijing.aliyuncs.com/' + candidate_value + '.jpg'
    # print(target_value)
    # print(random_obj)
    # print(caption_value)
    # print()
    user_ID = index_user
    index_user += 1
    return render_template('imgTxt.html',user_ID = user_ID, index_exp = index_exp, target_value=target_value, candidate_value=candidate_value, caption_value=caption_value)

@app.route('/img')
def index2():
    with open('static/initial.json', 'r') as f:
        data = json.load(f)
    random_obj = random.choice(data)
    target_value = random_obj['target']
    candidate_value = random_obj['candidate']
    target_value = 'https://fashion-iq.oss-cn-beijing.aliyuncs.com/' + target_value + '.jpg'
    candidate_value = 'https://fashion-iq.oss-cn-beijing.aliyuncs.com/' + candidate_value + '.jpg'
    print(target_value)
    print(random_obj)
    print()
    return render_template('image.html', target_value=target_value, candidate_value=candidate_value)


@app.route('/txt')
def index3():
    with open('static/initial.json', 'r') as f:
        data = json.load(f)
    random_obj = random.choice(data)
    target_value = random_obj['target']
    # candidate_value = random_obj['candidate']
    caption_value = random.choice(random_obj['captions'])
    caption_value = trans.translate_2_zh(caption_value)
    target_value = 'https://fashion-iq.oss-cn-beijing.aliyuncs.com/' + target_value + '.jpg'
    # candidate_value = 'https://fashion-iq.oss-cn-beijing.aliyuncs.com/' + candidate_value + '.jpg'
    print(target_value)
    print(random_obj)
    print(caption_value)
    return render_template('txt.html', target_value=target_value, ccaption_value=caption_value)


# @app.route('/withdraw', methods=['POST'])
# def withdraw():
#     result = {
#         'image': random.choice(images)  # 随机返回一张图片
#     }
#     return jsonify(result)

@app.route("/searchT", methods=["POST"])
def searchT():
    # 获取搜索文本和参考图片的URL
    print("收到 searchT")
    data = request.json
    searchText = data["searchText"]
    print("搜索文本：", searchText)
    searchText = trans.translate_2_en(searchText)
    print(searchText)
    # 随机替换8张图片
    # refImageUrl= "245600258X.jpg"
    imgUrls = client.search_text(searchText)
    print(imgUrls)
    # imgUrls = random.sample(test_image_urls, 8)
    # 返回替换后的8张图片URL
    return jsonify({"imgUrls": imgUrls})

@app.route("/searchI", methods=["POST"])
def searchI():
    # 获取搜索文本和参考图片的URL
    data = request.json
    refImageUrl = data["refImageUrl"]
    print("参考图片URL：", refImageUrl)
    refImageUrl = refImageUrl[47:]
    print(refImageUrl)
    # 随机替换8张图片
    # refImageUrl= "245600258X.jpg"
    imgUrls = client.search_image(refImageUrl)
    print(imgUrls)
    # imgUrls = random.sample(test_image_urls, 8)
    # 返回替换后的8张图片URL
    return jsonify({"imgUrls": imgUrls})

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
    # 随机替换8张图片
    # refImageUrl= "245600258X.jpg"
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
    print(user_search_round_log)
    # imgUrls = random.sample(test_image_urls, 8)
    # 返回替换后的8张图片URL
    round_num += 1
    return jsonify({"imgUrls": imgUrls, "round_num": round_num-1})


@app.route("/matchIT", methods=["POST"])
def matchIT():
    global index_exp
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
    print(success_exp)
    index_exp += 1
    random_obj = random.choice(data1)
    target_value = random_obj['target']
    candidate_value = random_obj['candidate']
    caption_value = random.choice(random_obj['captions'])
    target_value = 'https://fashion-iq.oss-cn-beijing.aliyuncs.com/' + target_value + '.jpg'
    candidate_value = 'https://fashion-iq.oss-cn-beijing.aliyuncs.com/' + candidate_value + '.jpg'
    caption_value = trans.translate_2_zh(caption_value)
    response_data = {
        "index_exp":index_exp,
        "target_value":target_value,
        "candidate_value":candidate_value,
        "caption_value":caption_value,
    }
    print(response_data)
    return jsonify(response_data)
@app.route("/Next_exp", methods=["POST"])
def Next_exp():
    global round_num
    global index_exp
    if round_num <= 2:
        return_value = None
    else:
        index_exp += 1
        random_obj = random.choice(data1)
        target_value = random_obj['target']
        candidate_value = random_obj['candidate']
        caption_value = random.choice(random_obj['captions'])
        target_value = 'https://fashion-iq.oss-cn-beijing.aliyuncs.com/' + target_value + '.jpg'
        candidate_value = 'https://fashion-iq.oss-cn-beijing.aliyuncs.com/' + candidate_value + '.jpg'
        caption_value = trans.translate_2_zh(caption_value)
        response_data = {
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
        print(fail_exp)
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