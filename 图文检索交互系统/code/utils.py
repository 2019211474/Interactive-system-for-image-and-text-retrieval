import os
import json
import random

user_data = []

class Log(object):

    def __init__(self):
        self.log = {
            # "1":{"triplet":{"r", "m", "t", "M"},"click":"t"},  r t M都是文件名
        }

        try:
            self.users_log = self.load_users_log()
        except Exception as e:
            print(e)
            self.users_log = {}

        try:
            self.users_num = len(self.users_log.keys())
            self.users_num = self.users_num + 1
            print(f"Users_num : {self.users_num}")
        except Exception as e:
            print(e)
            self.users_num = 1

    def load_users_log(self):
        with open("users_log.json") as f:
            return json.load(f)
        # 比较实验数据保存
    def save(self, index):
        if index == 10:
            print(self.log)
            print(self.users_log)
            print(self.users_num)
            self.users_log[str(self.users_num)] = self.log
            file_name = 'users_log_compare.json'
            with open(file_name, 'w',encoding="utf-8") as f:
                json.dump(self.users_log, f,ensure_ascii=False, indent=2)
                f.write('\n')
            self.log = {}
            print("sucess save No.{} user's log".format(self.users_num))
            self.users_num = self.users_num + 1
            # json.dump users_log

    def add_triplet(self, index, triplet):
        self.log[str(index)] = triplet
        return self.log

    def get_triplet(self, index):
        return self.log[str(index - 1)]


class User_Log(object):

    def __init__(self):
        self.log = {
            # "1":{"triplet":{"r", "m", "t", "M"},"click":"t"},  r t M都是文件名
        }
        self.search_log = {

        }

    def add_triplet(self, index, triplet):
        self.log[str(index)] = triplet
        return self.log
    # 图文检索数据存储
    def save(self,UserID, exp_num, initial_value, search_log, end_value):
        print(UserID,exp_num,search_log)
        self.search_log.setdefault(str(UserID),{})[str(exp_num)] = {
            "initial_data": initial_value,
            "search_log": search_log,
            "end_data": end_value
        }
        file_name = 'search_log_target.json'
        with open(file_name, 'w',encoding="utf-8") as f:
            json.dump(self.search_log, f, ensure_ascii=False, indent=2)
            f.write('\n')
        # self.search_log["exp_num"] = {}
        print("sucess save")

class User_Log_base(object):

    def __init__(self):
        self.log = {
                # "1":{"triplet":{"r", "m", "t", "M"},"click":"t"},  r t M都是文件名
            }
        self.search_log = {

            }
    def add_triplet(self, index, triplet):
        self.log[str(index)] = triplet
        return self.log

    def save_baseModel(self,UserID, exp_num, initial_value, search_log, end_value):
        print(UserID,exp_num,search_log)
        self.search_log.setdefault(str(UserID),{})[str(exp_num)] = {
            "initial_data": initial_value,
            "search_log": search_log,
            "end_data": end_value
        }
        file_name = 'search_log_baseModle.json'
        with open(file_name, 'w',encoding="utf-8") as f:
            json.dump(self.search_log, f, ensure_ascii=False, indent=2)
            f.write('\n')
        # self.search_log["exp_num"] = {}
        print("sucess save")
# 以文搜图的数据保存
class User_Log_txt(object):

    def __init__(self):
        self.log = {
            # "1":{"triplet":{"r", "m", "t", "M"},"click":"t"},  r t M都是文件名
        }
        self.search_log_txt = {
        }
    def add_triplet(self, index, triplet):
        self.log[str(index)] = triplet
        return self.log

    def save(self,UserID, exp_num, initial_value, search_log, end_value):
        print(UserID,exp_num,search_log)
        self.search_log_txt.setdefault(str(UserID),{})[str(exp_num)] = {
            "initial_data_txt": initial_value,
            "search_log_txt": search_log,
            "end_data_txt": end_value
        }
        file_name = 'search_log_txt.json'
        with open(file_name, 'w',encoding="utf-8") as f:
            json.dump(self.search_log_txt, f, ensure_ascii=False, indent=2)
            f.write('\n')
        # self.search_log["exp_num"] = {}
        print("sucess save")
class User_Log_img(object):

    def __init__(self):
        self.log = {
            # "1":{"triplet":{"r", "m", "t", "M"},"click":"t"},  r t M都是文件名
        }
        self.search_log_img = {

        }

    def add_triplet(self, index, triplet):
        self.log[str(index)] = triplet
        return self.log

    def save(self,UserID, exp_num, initial_value, search_log, end_value):
        print(UserID,exp_num,search_log)
        self.search_log_img.setdefault(str(UserID),{})[str(exp_num)] = {
            "initial_data_img": initial_value,
            "search_log_img": search_log,
            "end_data_img": end_value
        }
        file_name = 'search_log_img.json'
        with open(file_name, 'w',encoding="utf-8") as f:
            json.dump(self.search_log_img, f, ensure_ascii=False, indent=2)
            f.write('\n')
        # self.search_log["exp_num"] = {}
        print("sucess save")


def get_images():
    a = []
    for i in os.listdir('./static/'):
        a.append(os.path.join('./static/', i))
    return a


def get_test_url(num):
    urls = []
    for i in range(num):
        url = random.choice(get_images())
        urls.append(url)
    return urls


if __name__ == '__main__':
    a = get_test_url(9)
    print(a)
