# -*- coding: utf-8 -
import math
from src import *
from src.shell import *
from prettytable import PrettyTable


class StartAndroid:

    # 启动App（冷/热启动命令相同），并获取启动时间
    def start(self, device_name, app_package, app_activity):
        stmt = "adb -s %s shell am start -W -n %s/%s" % (device_name, app_package, app_activity)
        result = subprocess_popen(stmt)
        time.sleep(3)  # 由于一些设备老旧、卡顿，需要给其反应时间
        return result

    # 热启动停止App（将APP至为后台）
    def hot_stop(self, device_name):
        stmt = "adb -s %s shell input keyevent 3" % device_name
        result = subprocess_popen(stmt)
        time.sleep(3)  # 由于一些设备老旧、卡顿，需要给其反应时间
        return result

    # 冷启动停止App（杀掉App后台）
    def cold_stop(self, device_name, app_package):
        stmt = "adb -s %s shell am force-stop %s" % (device_name, app_package)
        result = subprocess_popen(stmt)
        time.sleep(3)  # 由于一些设备老旧、卡顿，需要给其反应时间
        return result

    # 从启动命令结果中获取启动时间
    def get_start_time(self, device_name, app_package, app_activity):
        result = self.start(device_name, app_package, app_activity)
        for line in result:
            if "ThisTime" in line:
                start_time = line.split(":")[1]
                return start_time

    # 执行App冷热启动
    def start_report(self, device_name, app_package, app_activity, num):
        try:
            print("\nAPP启动报告:")
            result1 = PrettyTable(["冷启动", "startTime(ms)", "timestamp"])
            result2 = PrettyTable(["热启动", "startTime(ms)", "timestamp"])
            n1 = 0
            n2 = 0
            for i in range(num):
                n1 += 1
                result1.add_row([n1, self.get_start_time(device_name, app_package, app_activity), get_current_time()])
                time.sleep(20)  # 冷启动需要加载大量数据，设置等待时间使其加载完成
                for n in range(4):
                    n2 += 1
                    self.hot_stop(device_name)
                    result2.add_row([n2, self.get_start_time(device_name, app_package, app_activity), get_current_time()])
                self.cold_stop(device_name, app_package)
            print(result1, "\n\n\n", result2)
        except:
            print("APP启动测试失败")


class Start:
    def __init__(self, *parm):
        self.android = StartAndroid()
        if parm[0] is None:
            self.num = 1
        else:
            self.num = int(parm[0])

    def start(self, app_name, device_name):
        app_info = ReadConfigFile(android_path).get_info('app', app_name)
        device_info = ReadConfigFile(android_path).get_info('device', device_name)
        self.android.start_report(device_info['deviceName'], app_info['appPackage'], app_info['appActivity'], self.num)
