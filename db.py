import redis
import random
from .config import *


class RedisClient(object):
    def __init__(self, type, website, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        self.db = redis.StrictRedis(host, port, password, decode_responses=True)
        # Hash名称类型accounts或者cookies
        self.type = type
        # 站点weibo、zhihu等
        self.website = website

    def name(self):
        """
        获取Hash名称 如：accounts:weibo  (type=accounts, website=weibo)
        :return: Hash名称 如：accounts:weibo
        """

        return '{type}:{website}'.format(type=self.type, website=self.website)

    def set(self, username, value):
        """
        设置键值对
        :param username: 账号
        :param value: 密码或者cookies
        :return:
        """
        return self.db.hset(self.name(), username, value)

    def get(self, username):
        """
        根据key获取value
        :param username: key
        :return: key对应的value
        """
        return self.db.hget(self.name(), username)

    def delete(self, username):
        """
        根据key删除键值对
        :param username: key
        :return: 删除的结果
        """
        return self.db.hdel(self.name(), username)

    def count(self):
        """
        获取键值对的数量
        :return:
        """
        return self.db.hlen(self.name())

    def random(self):
        """
        随机获取一个值value，主要用于随机获取一个cookies
        :return:
        """
        return random.choice(self.db.hvals(self.name()))

    def usernames(self):
        """
        获取所有的key 用户名
        :return:
        """
        return self.db.hkeys(self.name())

    def all(self):
        """
        获取所有的键值对
        :return:
        """
        return self.db.hgetall(self.name())
