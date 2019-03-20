from .db import RedisClient
from fake_useragent import UserAgent
import json
from .config import *
import requests


class ValidTester(object):
    def __init__(self, website):
        self.website = website
        self.account_db = RedisClient('accounts', self.website)
        self.cookies_db = RedisClient('cookies', self.website)
        self.headers = {
            'User-Agent': UserAgent(verify_ssl=False).random
        }

    def test(self, username, cookies):
        raise NotImplementedError

    def run(self):
        print('Cookies开始检测')
        cookies_groups = self.cookies_db.all()
        for username, cookies in cookies_groups.items():
            self.test(username, cookies)


class WeiBoValidTester(ValidTester):
    def __init__(self, website='weibo'):
        ValidTester.__init__(self, website)

    def test(self, username, cookies):
        print('正在检测的%s用户的cookies' % username)
        try:
            cookies = json.loads(cookies)
        except TypeError:
            print('该用户%s的cookies%s格式不对' % (username, cookies))
            self.cookies_db.delete(username)
            print('删除cookies')
            return
        try:
            url = TEST_URL_MAP[self.website]
            response = requests.get(url, headers=self.headers, cookies=cookies, allow_redirects=False)
            if response.status_code == 200:
                print('用户%s的cookies有效' % username)
            else:
                print('用户%s的cookies失效' % username)
                self.cookies_db.delete(username)
                print('删除cookies')
        except ConnectionError as ce:
            print('异常', ce.args)
