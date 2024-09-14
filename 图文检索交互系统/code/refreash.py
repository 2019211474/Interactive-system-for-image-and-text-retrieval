import os
import json

# 指定JSON文件所在的目录
directory = r'C:\Users\Admin\Desktop\熊志鹏工作空间\flaskProject2'

# 遍历目录中的所有文件
for filename in os.listdir(directory):
    filepath = os.path.join(directory, filename)

    # 仅处理以 "search" 或 "users_log" 开头的JSON文件
    if filename.startswith("search") or filename.startswith("users_log"):
        # 清空JSON文件
        with open(filepath, 'w') as file:
            json.dump({}, file)
            print(f"Cleared: {filepath}")
