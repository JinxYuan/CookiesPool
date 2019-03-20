from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time


class WeiBoLogin(object):
    def __init__(self, username, password, brower):
        self.url = 'https://passport.weibo.cn/signin/login?entry=mweibo&r=https://m.weibo.cn/'
        self.browser = brower
        self.wait = WebDriverWait(self.browser, 15)
        self.username = username
        self.password = password

    # def __del__(self):
    #     self.browser.close()

    def open(self):
        self.browser.get(self.url)
        time.sleep(1)
        username = self.wait.until(EC.presence_of_element_located((By.ID, 'loginName')))
        time.sleep(1)
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'loginPassword')))
        submit = self.wait.until(EC.element_to_be_clickable((By.ID, 'loginAction')))
        time.sleep(3)
        username.send_keys(self.username)
        password.send_keys(self.password)
        print('login', self.username, self.password)
        time.sleep(2)
        submit.click()

    def password_error(self):
        return bool(self.wait.until(EC.presence_of_element_located((By.ID, 'errorMsg'))))

    def get_cookies(self):
        print(self.browser.get_cookies())
        return self.browser.get_cookies()

    def login_success(self):
        return bool(
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'lite-iconf-profile')))
        )

    def main(self):
        self.open()
        time.sleep(5)
        print('login_main')
        if self.login_success():
            return {
                'status': 1,
                'content': self.get_cookies()
            }
        elif self.password_error():
            return {
                'status': 2,
                'content': '账号密码错误'
            }
        else:
            return {
                'status': 3,
                'content': '登录失败'
            }


# from selenium import webdriver
#
# if __name__ == '__main__':
#     login = WeiBoLogin('your username', 'your password', webdriver.Chrome())
#     login.main()
