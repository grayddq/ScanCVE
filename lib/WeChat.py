# -*- coding: utf-8 -*-

import requests
import json


class WeChat:
    def __init__(self, CORPID, CORPSECRET, AGENTID, TOUSER):
        self.CORPID = CORPID  # 企业ID，在管理后台获取
        self.CORPSECRET = CORPSECRET  # 自建应用的Secret，每个自建应用里都有单独的secret
        self.AGENTID = AGENTID  # 应用ID，在后台应用中获取
        self.TOUSER = TOUSER  # 接收者用户名,多个用户用|分割

    def get_access_token(self):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        values = {'corpid': self.CORPID,
                  'corpsecret': self.CORPSECRET,
                  }
        req = requests.post(url, params=values)
        data = json.loads(req.text)
        return data["access_token"]

    def send_data(self, message):
        send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + self.get_access_token()
        send_values = {
            "touser": self.TOUSER,
            "msgtype": "text",
            "agentid": self.AGENTID,
            "text": {
                "content": message
            },
            "safe": "0"
        }
        # send_values = {
        #     "touser": self.TOUSER,
        #     "msgtype": "markdown",
        #     "agentid": self.AGENTID,
        #     "markdown": {
        #         "content": message
        #     },
        #     "safe": "0"
        # }
        send_msges = (bytes(json.dumps(send_values)))
        respone = requests.post(send_url, send_msges)
        respone = respone.json()  # 当返回的数据是json串的时候直接用.json即可将respone转换成字典
        return respone["errmsg"]


if __name__ == '__main__':
    wx = WeChat('wx4fd7e9327739aafa','','1000003','@all')
    # wx.send_data("这是程序发送的第1条消息！\n Python程序调用企业微信API")
    wx.send_data("这是程序发送的第2条消息！")
