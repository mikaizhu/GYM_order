import requests
from bs4 import BeautifulSoup
import os
import ddddocr
from datetime import datetime


class GYM:
    def __init__(self, username, password):
        self.userID = username
        self.pw = password

    def login(self):
        s = requests.Session()
        logInfo_ = {
                'username':self.userID,
                'password':self.pw,
                'Origin':'https://authserver.szu.edu.cn',
                'ts':
                }
        header = {
            'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36'
        }
        url = "https://authserver.szu.edu.cn/authserver/login?service=http%3A%2F%2Fehall.szu.edu.cn%2Flogin%3Fservice%3Dhttp%3A%2F%2Fehall.szu.edu.cn%2Fnew%2Findex.html"
        req = s.post(url, headers=header, data=logInfo_)
        #print(req.text)
        logInfo_ = self.parserValidateCode(s, logInfo_)
        #soup = BeautifulSoup(req.text, 'html.parser')
        req = s.post(url, data=logInfo_)
        print(req.status_code)
        print(req.text)

    def parserValidateCode(self, s, logInfo_):
        # 验证码识别部分, 如果有验证码，则添加信息
        # 先获取验证码, 并保存到本地
        ts = str(round(datetime.now().microsecond/10**3))
        verify_code_url = 'https://authserver.szu.edu.cn/authserver/captcha.html?ts=' + ts
        code_response = s.get(url=verify_code_url, data=logInfo_, verify=False)
        with open('verify.png', mode='wb') as f:
            f.write(code_response.content)
        ocr = ddddocr.DdddOcr()
        with open('verify.png', 'rb') as f:
            img_bytes = f.read()
        verify_code = ocr.classification(img_bytes)
        os.remove('verify.png')
        logInfo_['captchaResponse'] = verify_code
        return logInfo_

username = '2070436044'
password = '12180030'
gym = GYM(username, password)
gym.login()
