import os
import json
import random
test_50_triplets={
    "1":[],
    "2":[],

}

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


    def save(self, index):
        if index == 3:
            # print("333333")
            print(self.log)
            print(self.users_log)
            print(self.users_num)
            self.users_log[str(self.users_num)] = self.log
            file_name = 'users_log.json'
            with open(file_name, 'w') as f:
                json.dump(self.users_log, f)
                f.write('\n')
            self.log = {}
            print("sucess save No.{} user's log".format(self.users_num))
            self.users_num = self.users_num + 1
            # json.dump users_log

    def add_triplet(self, index, triplet):
        self.log[str(index)] = triplet
        return self.log

    def get_triplet(self, index):
        return self.log[str(index-1)]

class User_Log(object):

    def __init__(self):
        self.log = {
            # "1":{"triplet":{"r", "m", "t", "M"},"click":"t"},  r t M都是文件名
        }

    def add_triplet(self, index, triplet):
        self.log[str(index)] = triplet
        return self.log

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