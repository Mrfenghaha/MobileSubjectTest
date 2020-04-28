# -*- coding: utf-8 -
import math
from src import *
from src.shell import *
from prettytable import PrettyTable


class MemoryUsageAndroid:

    # adb命令获取设备整体内存
    def total_memory_usage(self, device_name):
        stmt = "adb -s %s shell cat /proc/meminfo | %s MemTotal" % (device_name, query)
        result = subprocess_popen(stmt)
        return result

    # adb命令获取应用详细的内存使用情况PSS
    def app_memory_usage(self, device_name, app_package):
        stmt = "adb -s %s shell dumpsys meminfo %s" % (device_name, app_package)
        result = subprocess_popen(stmt)
        return result

    # adb命令获取APP占用内存情况
    def get_total_memory_usage(self, device_name):
        result = self.total_memory_usage(device_name)
        memory = result[0].split(":")[1].split("k")[0].strip(" ")
        return memory

    # adb命令获取APP占用内存情况
    def get_app_memory_usage(self, device_name, app_package):
        result = self.app_memory_usage(device_name, app_package)
        if result is []:
            return 0
        else:
            for line in result:
                if "TOTAL:" in line:
                    res = line
            memory = res.split("TOTAL")[1].strip(":").strip(" ")
            return memory

    def memory_usage_report(self, device_name, app_package, num):
        try:
            total_memory = self.get_total_memory_usage(device_name)
            result = PrettyTable(["serialNumber", "memory(kb)", "timestamp"])
            for i in range(1, num + 1):
                memory = self.get_app_memory_usage(device_name, app_package)
                result.add_row([i, memory, get_current_time()])
                time.sleep(3)  # 每间隔3s获取一次
            print("\n内存占用报告:")
            print("设备总内存: %skb(%sG)" % (total_memory, "%.2f" % (int(total_memory)/1024/1024)))
            print(result)
        except:
            print("内存测试失败")


class MemoryUsage:
    def __init__(self, *parm):
        self.android = MemoryUsageAndroid()
        if parm[0] is None:
            self.num = 1
        else:
            self.num = math.floor(int(parm[0]) / 3)

    def memory_usage_android(self, app_name, device_name):
        app_info = ReadConfigFile(android_path).get_info('app', app_name)
        device_info = ReadConfigFile(android_path).get_info('device', device_name)
        self.android.memory_usage_report(device_info['deviceName'], app_info['appPackage'], self.num)
