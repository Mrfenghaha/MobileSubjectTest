# -*- coding: utf-8 -
import math
from src import *
from src.shell import *
from prettytable import PrettyTable


class TemperatureAndroid:

    # adb命令获取APP电池温度
    def temperature(self, device_name):
        stmt = "adb -s %s shell dumpsys battery | %s temperature" % (device_name, query)
        result = subprocess_popen(stmt)
        return result

    def get_temperature(self, device_name):
        result = self.temperature(device_name)
        temperature = result[0].split(":")[1].strip(" ")
        return temperature

    def temperature_report(self, device_name, num):
        try:
            result = PrettyTable(["serialNumber", "temperature(℃)", "timestamp"])
            for i in range(num):
                temperature = int(self.get_temperature(device_name)) / 10
                result.add_row([i+1, temperature, get_current_time()])
                time.sleep(3)  # 每间隔3s获取一次
            print("\n电池温度报告:")
            print(result)
        except:
            print("电池温度测试失败")


class Temperature:
    def __init__(self, *parm):
        self.android = TemperatureAndroid()
        if parm[0] is None:
            self.num = 1
        else:
            self.num = math.floor(int(parm[0]) / 3)

    def temperature_android(self, device_name):
        device_info = ReadConfigFile(android_path).get_info('device', device_name)
        self.android.temperature_report(device_info['deviceName'], self.num)
