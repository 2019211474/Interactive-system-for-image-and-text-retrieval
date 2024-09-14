import json
# 读取JSON文件
with open('search_log_baseModle.json', 'r', encoding='utf-8') as file:
    # with open('search_log_target.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
# 统计一级节点数量
print(" 图文检索（baseline）被试用户数量:", len(data.keys()))
for key in data.keys():
    print('用户', key, '的实验条数：', len(data[key].keys()))
print('-------------------------------')
# 读取JSON文件
# with open('search_log_baseModle.json', 'r', encoding='utf-8') as file:
with open('search_log_target.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 统计一级节点数量
print("     图文检索（ours）被试用户数量:", len(data.keys()))
for key in data.keys():
    print('用户', key, '的实验条数：', len(data[key].keys()))

print('-------------------------------')
with open('search_log_img.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
print("            图片检索被试用户数量:", len(data.keys()))
for key in data.keys():
    print('用户', key, '的实验条数：', len(data[key].keys()))

print('-------------------------------')
with open('search_log_txt.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
print("            文本检索被试用户数量:", len(data.keys()))
for key in data.keys():
    print('用户', key, '的实验条数：', len(data[key].keys()))

print('-------------------------------')
with open('users_log_compare.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
print("            对比实验被试用户数量:", len(data.keys()))
for key in data.keys():
    print('用户', key, '的实验条数：', len(data[key].keys()))