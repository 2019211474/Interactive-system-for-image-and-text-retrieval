import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tmt.v20180321 import tmt_client, models

class Translator(object):
    def __init__(self):
        # cred = credential.Credential("SecretId", "SecretKey")
        self.cred = credential.Credential("AKIDlMincGdjY6NN6ZmiNmulLegS4PTHo43l", "SdYCZfU2JK4WidGdjY6NM5YkeHdjZHju")
        self.httpProfile = HttpProfile()
        self.httpProfile.endpoint = "tmt.tencentcloudapi.com"

        # 实例化一个client选项，可选的，没有特殊需求可以跳过
        self.clientProfile = ClientProfile()
        self.clientProfile.httpProfile = self.httpProfile
        # 实例化要请求产品的client对象,clientProfile是可选的
        self.client = tmt_client.TmtClient(self.cred, "ap-shanghai", self.clientProfile)

    def translate_2_en(self, zh_text):
        req = models.TextTranslateBatchRequest()
        params = {
            "Source": "auto",
            "Target": "en",
            "ProjectId": 0,
            "SourceTextList": [zh_text]
        }
        req.from_json_string(json.dumps(params))
        try:
            resp = self.client.TextTranslateBatch(req)
            resp = resp.to_json_string()
            resp = json.loads(resp)
            # print(resp)
            # print(type(resp))
            return resp['TargetTextList'][0]
        except Exception as e:
            print(e)

    def translate_2_zh(self, en_text):
        req = models.TextTranslateBatchRequest()
        params = {
            "Source": "en",
            "Target": "zh",
            "ProjectId": 0,
            "SourceTextList": [en_text]
        }
        req.from_json_string(json.dumps(params))
        try:
            resp = self.client.TextTranslateBatch(req)
            resp = resp.to_json_string()
            resp = json.loads(resp)
            # print(resp)
            # print(type(resp))
            return resp['TargetTextList'][0]
        except Exception as e:
            print(e)

if __name__ == '__main__':
    trans = Translator()
    a  =  trans.translate_2_zh('hello worlld')
    print(a)