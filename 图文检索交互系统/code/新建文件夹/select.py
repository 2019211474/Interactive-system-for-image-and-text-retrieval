import json

# 读取原始的JSON文件
with open('C:\Users\Admin\Desktop\熊志鹏工作空间\flaskProject2\static\initial.json', 'r') as f:
    data = json.load(f)

# 选择前20个元素
selected_data = data[:20]

# 将选中的元素保存到新的JSON文件
with open('output.json', 'w', encoding='utf-8') as f:
    json.dump(selected_data, f, ensure_ascii=False, indent=2)
