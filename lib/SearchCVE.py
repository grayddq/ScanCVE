# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from translate import Translator


# 根据给予的cve编号查询cve描述信息，并进行翻译
class SearchCVE:
    def __init__(self, CVE):
        self.CVE = CVE
        # self.url = "http://cve.mitre.org/cgi-bin/cvename.cgi?name={}".format(self.CVE)
        self.url = "https://nvd.nist.gov/vuln/detail/{}".format(self.CVE)
        self.context = ""
        self.score = ""

    # 获取
    # def get_cve_description(self):
    #     response = requests.get(self.url).text
    #     soup = BeautifulSoup(response, "lxml")
    #     if 'ERROR' in soup.title.text:
    #         return False, "未查询到CVE信息"
    #     desc = soup.body.findAll('td')
    #     if "RESERVED" in desc[10].text:
    #         return False, "未公开描述"
    #     return True, desc[10].text

    def fanyi(self, context):
        translator = Translator(to_lang="chinese")
        translation = translator.translate(context)
        return translation

    def run(self):
        self.get_cve_description()
        if self.context != "未查询到CVE信息".decode('utf-8'):
            self.context = self.fanyi(self.context)
        if self.score != "暂无".decode('utf-8'):
            self.score = self.fanyi(self.score)

        return self.score, self.context

    def get_cve_description(self):

        response = requests.get(self.url).text
        soup = BeautifulSoup(response, "lxml")

        description = soup.body.findAll('p', {'data-testid': "vuln-description"})
        self.context = description[0].text.replace("** DISPUTED **", "") if len(description) == 1 else "未查询到CVE信息".decode('utf-8')

        cvss = soup.body.findAll('a', {'data-testid': "vuln-cvss3-panel-score"})
        self.score = cvss[0].text if len(cvss) == 1 else "暂无".decode('utf-8')


if __name__ == '__main__':
    s = SearchCVE("CVE-2020-09761")
    score, context = s.run()
    print score
    print context
