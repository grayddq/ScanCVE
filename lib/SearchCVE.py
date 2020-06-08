# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from translate import Translator


# 根据给予的cve编号查询cve描述信息，并进行翻译
class SearchCVE:
    def __init__(self, CVE):
        self.CVE = CVE
        self.url = "http://cve.mitre.org/cgi-bin/cvename.cgi?name={}".format(self.CVE)

    # 获取
    def get_cve_description(self):
        response = requests.get(self.url).text
        soup = BeautifulSoup(response, "lxml")
        if 'ERROR' in soup.title.text:
            return False, "未查询到CVE信息"
        desc = soup.body.findAll('td')
        if "RESERVED" in desc[10].text:
            return False, "未公开描述"
        return True, desc[10].text

    def fanyi(self, context):
        translator = Translator(to_lang="chinese")
        translation = translator.translate(context)
        return translation

    def run(self):
        s, context = self.get_cve_description()
        if s: context = self.fanyi(context)
        return context


if __name__ == '__main__':
    s = SearchCVE("CVE-2020-0976")
    print s.run()
