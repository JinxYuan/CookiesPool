# CookiesPool
CookiesPool用于需要登录的时候
# config.py
TEST_URL_MAP更改为自己需要登录的网站
REDIS_HOST、REDIS_PASSWORD更改为自己的redis地址、密码和端口号
# generator.py
1. 创建自己的网站class继承CookiesGenerator
2. 我这里是微博的class WeiBoCookiesGenerator(CookiesGenerator):
# login.py
1. 我这里用的selenium获取Cookies 
2. 这里需要改成自己的网站登录
3. 创建自己的登录class(class WeiBoLogin(object):)
# tester.py
1. 这里可以创建自己的测试class继承ValidTester
2.
```
class WeiBoValidTester(ValidTester):
    # 站点改为自己的
    def __init__(self, website='weibo'):
        ValidTester.__init__(self, website)
```
# 使用
1. 使用前，先运行importe.py文件
2. 输入自己需要登录的网站的账号密码(格式为：账号 密码)
3. 运行scheduler.py文件
```
def get_random_cookies(self):
    # http://API_HOST:API_PORT/website/random
    self.cookies_url = 'http://127.0.0.1:5000/weibo/random'
    try:
        response = requests.get(self.cookies_url)
        if response.status_code == 200:
            cookies = json.loads(response.text)
            return cookies
    except requests.ConnectionError as e:
        print('cookies', e.args)
        return False

def process_request(self, request, spider):
    self.logger.debug('正在获取 Cookies')
    cookies = self.get_random_cookies()
    if cookies:
        request.cookies = cookies
```
