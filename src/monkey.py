# -*- coding: utf-8 -
import math
from src import *
from src.shell import *
# 创建monkeyReport文件夹
CreateFile(monkey_report_path).create_folder()


class MonkeyAndroid:

    # adb命令执行monkey测试
    def monkey(self, device_name, app_package, num, info_log, error_log):
        stmt = "adb -s %s shell monkey -p %s -v -v -v --throttle 100 --ignore-crashes --ignore-timeouts " \
               "--ignore-security-exceptions --ignore-native-crashes %s -s 1>>%s 2>>%s" % \
               (device_name, app_package, num, info_log, error_log)
        result = subprocess_popen(stmt)
        return result

    # 中途停止monkey测试ßß
    def kill_monkey(self, device_name):
        stmt = "adb -s %s shell ps | %s monkey" % (device_name, query)
        pid = subprocess_popen(stmt).split()[1]
        stmt = "adb -s %s shell kill %s" % (device_name, pid)
        subprocess_popen(stmt)

    def monkey_test(self, device_name, app_package, num):
        now = time.strftime("%Y%m%d%H%M%S")
        info_log = os.path.join(monkey_report_path, now + "info.txt")
        error_log = os.path.join(monkey_report_path, now + "error.txt")
        self.monkey(device_name, app_package, num, info_log, error_log)


class Monkey:
    def __init__(self, *parm):
        self.android = MonkeyAndroid()
        if parm[0] is None:
            self.num = 200
        else:
            self.num = math.floor(int(parm[0]) / 0.05)  # 每一次执行回间隔0.5秒

    def monkey(self, app_name, device_name):
        app_info = ReadConfigFile(android_path).get_info('app', app_name)
        device_info = ReadConfigFile(android_path).get_info('device', device_name)
        self.android.monkey_test(device_info['deviceName'], app_info['appPackage'], self.num)
