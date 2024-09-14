import requests
from flask import request

from trans import Translator

# 定义服务器URL
server = 'http://10.200.90.59:8991'  # 修改为你的服务器URL
# def search_image(image_name):
    # 定义服务器URL
    # server = 'http://10.200.90.59:8999'  # 修改为你的服务器URL
    #
    # url = server + '/searchImageI'  # image search
    # # image_name = "245600258X.jpg"  # 修改为你的图片名称
    # response = requests.get(url, params={'image_name': image_name})
    # # 解析响应
    # result = response.json()
    # print("图片搜索服务器返回的结果：", result["result"])
    # return result


# url = server + '/searchImageT'  # text search
# text = "a blue shirt"  # 修改为你的图片名称
# response = requests.get(url, params={'text': text})
# result = response.json()
# print("以文搜图服务器返回的结果：", result["result"])
#
def search_text_image(text,image_name):
    url = server + '/searchImageIT'  # text search

    response = requests.get(url, params={'text': text, 'image_name': image_name})
    result = response.json()
    print("图文检索服务器返回的结果：", result["result"])
    return result


def search_text_image2(text,image_name):
    url = server + '/searchImageIT2'  # text search
    # text = "a blue shirt"
    # image_name = "245600258X.jpg"  # 修改为你的图片名称
    response = requests.get(url, params={'text': text, 'image_name': image_name})
    result = response.json()
    print("图文检索服务器返回的结果：", result["result"])
    return result

def search_image(image_name):
    url = server + '/searchImageI'  # text search
    # text = "a blue shirt"
    # image_name = "245600258X.jpg"  # 修改为你的图片名称
    response = requests.get(url, params={'image_name': image_name})
    result = response.json()
    print("图文检索服务器返回的结果：", result["result"])
    return result


def search_text(text):
    url = server + '/searchImageT'  # text search
    # text = "a blue shirt"
    # image_name = "245600258X.jpg"  # 修改为你的图片名称
    response = requests.get(url, params={'text': text})
    result = response.json()
    print("图文检索服务器返回的结果：", result["result"])
    return result



if __name__ == '__main__':
    # search_image("245600258X.jpg")
    # search_text("dog")
    search_text_image("dog","245600258X.jpg")
    # search_text_image2("dog","245600258X.jpg")
