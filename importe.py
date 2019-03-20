from .db import RedisClient

conn = RedisClient('accounts', 'weibo')


def set_username_password(account):
    username, password = account.split(' ')
    result = conn.set(username, password)
    print('账号：%s，密码：%s' % (username, password))
    print('录入成功' if result else '录入失败')


def scan():
    print('输入账号密码(格式：账号 密码)，输入exit退出')
    while 1:
        account = input()
        if account == 'exit':
            break
        set_username_password(account)


if __name__ == '__main__':
    scan()
