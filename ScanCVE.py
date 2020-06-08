# -*- coding:utf-8 -*-

import ConfigParser
from lib.WeChat import *
from lib.ScanGitHub import *
import os

if __name__ == '__main__':
    syspath = os.path.dirname(os.path.abspath(__file__))
    conf = ConfigParser.ConfigParser()
    conf.read(syspath + "/conf/info.conf")

    CORPID = conf.get("WeChat", "CORPID").strip()
    CORPSECRET = conf.get("WeChat", "CORPSECRET").strip()
    AGENTID = conf.get("WeChat", "AGENTID").strip()
    TOUSER = conf.get("WeChat", "TOUSER").strip()
    times = int(conf.get("Time", "time").strip())
    while True:
        try:
            # 获取增量cve信息
            context = ScanGitHubCVE(syspath).getAddNews
            # 当记录数量有变化时，进行消息推送
            if context != "":
                print context
                # 推送微信消息
                wx = WeChat(CORPID, CORPSECRET, AGENTID, TOUSER)
                wx.send_data(context)
            # 等待一定时间
            time.sleep(times)
        except:
            time.sleep(times)
