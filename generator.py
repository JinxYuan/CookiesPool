from .db import RedisClient
from .login import WeiBoLogin
from selenium import webdriver
import json


class CookiesGenerator(object):
    def __init__(self, website):
        self.website = website
        self.accounts_db = RedisClient('accounts', self.website)
        self.cookies_db = RedisClient('cookies', self.website)
        self.browser = webdriver.Chrome()

    def new_cookies(self, username, password):
        raise NotImplementedError

    @staticmethod
    def process_cookies(cookies):
        dic = {}
        for cookie in cookies:
            dic[cookie['name']] = cookie['value']
        return dic

    def run(self):
        accounts_username = self.accounts_db.usernames()
        print('generator_accounts', accounts_username)
        cookies_username = self.cookies_db.usernames()
        print('generator_cookies', cookies_username)
        for username in accounts_username:
            print('generator_for')
            if username not in cookies_username:
                print('username not in cookies_username')
                password = self.accounts_db.get(username)
                print('password:%s' % password)
                result = self.new_cookies(username, password)
                print('generator_if', result)
                if result.get('status') == 1:
                    cookies = self.process_cookies(result.get('content'))
                    print('获取cookies成功', cookies)
                    if self.cookies_db.set(username, json.dumps(cookies)):
                        print('cookies保存成功')
                elif result.get('status') == 2:
                    if self.accounts_db.delete(username):
                        print('账号、密码删除成功')
                else:
                    print(result.get('content'))
        else:
            print('所有账号都获取了cookies')

    def close(self):
        try:
            print('关闭浏览器')
            self.browser.close()
        except TypeError:
            print('浏览器操作失败')


class WeiBoCookiesGenerator(CookiesGenerator):
    def __init__(self, website="weibo"):
        CookiesGenerator.__init__(self, website)
        self.website = website

    def new_cookies(self, username, password):
        return WeiBoLogin(username, password, self.browser).main()


# if __name__ == '__main__':
#     a = WeiBoCookiesGenerator(website='weibo')
#     a.run()
