from yjx_project.CookiesPool.cookiespool.config import *
import time
from yjx_project.CookiesPool.cookiespool.api import app
from multiprocessing import Process
from yjx_project.CookiesPool.cookiespool.generator import WeiBoCookiesGenerator
from yjx_project.CookiesPool.cookiespool.tester import WeiBoValidTester


class Scheduler(object):
    @staticmethod
    def valid_cookies(cycle=CYCLE):
        while 1:
            print('Cookies检测')
            try:
                for website, cls in TEST_MAP.items():
                    tester = eval(cls+'(website="'+website+'")')
                    print(tester)
                    tester.run()
                    print('检测完成')
                    del tester
                    time.sleep(cycle)
            except Exception as e:
                print('调度器valid_cookies', e.args)

    @staticmethod
    def generator_cookies(cycle=CYCLE):
        while 1:
            print('开始生成cookies')
            try:
                for website, cls in GENERATOR_MAP.items():
                    generator = eval(cls+'(website="'+website+'")')
                    generator.run()
                    print('cookies生成完成')
                    generator.close()
                    time.sleep(cycle)
            except Exception as e:
                print('调度器generator_cookies', e.args)

    @staticmethod
    def api():
        print('接口开始运行')
        app.run(host=API_HOST, port=API_PORT)

    @staticmethod
    def run():
        if VALID_PROCESS:
            valid_process = Process(target=Scheduler.valid_cookies)
            valid_process.start()

        if GENERATOR_PROCESS:
            generator_process = Process(target=Scheduler.generator_cookies)
            generator_process.start()

        if API_PROCESS:
            api_process = Process(target=Scheduler.api)
            api_process.start()


Scheduler().run()
