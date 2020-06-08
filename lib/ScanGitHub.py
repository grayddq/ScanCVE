# -*- coding: utf-8 -*-

import requests
import json, time, re
from operator import itemgetter
from SearchCVE import *

import sys

reload(sys)
sys.setdefaultencoding('utf8')


class ScanGitHubCVE:
    def __init__(self, path):
        self.dbjson = path + "/db/db.json"
        self.total = self.loadDB()
        self.year = time.strftime("%Y", time.localtime(time.time()))
        return

    def loadDB(self):
        with open(self.dbjson, 'r') as load_f:
            data = json.load(load_f)
            total = data['total_count']
            return total
        return 0

    # 得到所有cve信息
    def _getNewsAll(self):
        try:
            api = "https://api.github.com/search/repositories?q=CVE-{}&sort=updated".format(self.year)
            response = requests.get(api).text
            data = json.loads(response)
            return data
        except Exception as e:
            print(e, "Github链接不通")

    # 得到增量cve信息
    @property
    def getAddNews(self):
        data = self._getNewsAll()
        content = ""  # 待发送内容
        if data['total_count'] <= self.total:
            return content

        content = "【CVE新增监控告警】"
        count = data['total_count'] - self.total
        self.updateDB(data)
        items = sorted(data['items'], key=itemgetter('id'), reverse=True)
        for i in range(count):
            # 当更新大于5个时，只显示前5个
            if i == 5: return content
            item = items[i]
            git_name = item['name']
            git_url = item['svn_url']
            git_des = item['description'] if item['description'] else "Null"
            # 提取git名称中的cve编号，匹配第一个
            cve_name, cve_des = "未知编号", ""
            if len(re.findall('(?i)cve-2020-\d*', git_name)) > 0:
                cve_name = re.findall('(?i)cve-2020-\d*', git_name)[0]
            # 提取git描述中的cve编号，匹配第一个
            else:
                if len(re.findall('(?i)cve-2020-\d*', git_des)) > 0:
                    cve_name = re.findall('(?i)cve-2020-\d*', git_des)[0]
            # 获取cve漏洞说明
            cve_des = "" if cve_name == "" else SearchCVE(cve_name).run()

            content += "\n[{}] 项目名称：{}\n[{}] 项目描述: {}\n[{}] CVE编号：{}\n[{}] CVE说明：{}\n".format(
                i, '<a href=\"' + git_url + '\">' + git_name + '</a>', i, git_des, i, cve_name, i, cve_des)

        return content

    def updateDB(self, data):
        with open(self.dbjson, "w") as f:
            json.dump(data, f)
        return


if __name__ == '__main__':
    s = ScanGitHubCVE("/Users/grayddq/Grayddq/01.mygit/22.gitScanCve")
    print s.getAddNews
