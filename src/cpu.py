# -*- coding: utf-8 -
import math
from src import *
from src.shell import *
from prettytable import PrettyTable


class CPUUsageAndroid:

    # adb命令获取APP占用CPU情况
    def cpu_usage(self, device_name, app_package):
        stmt = "adb -s %s shell dumpsys cpuinfo | %s %s" % (device_name, query, app_package)
        result = subprocess_popen(stmt)
        return result

    def get_cpu_usage(self, device_name, app_package):
        result = self.cpu_usage(device_name, app_package)
        if result is False:
            # print("未获取到cpu数据，请操作应用程序")
            return "null", "null", "null", "null"  # 当无法获取cpu数据时使用null表示所有值
        else:
            cpu_value = result[0].split("%")
            cpu = cpu_value[0].strip(" ").strip("+")
            user = cpu_value[1].split("/")[1].split(":")[1].strip(" ")
            kernel = cpu_value[2].split("+")[1].strip(" ")
            if len(result[0].split("/")) == 3:
                faults = cpu_value[3].split("/")[1].split(":")[1]
            else:
                faults = "null"
            return cpu, user, kernel, faults

    def cpu_usage_report(self, device_name, app_package, num):
        try:
            result = PrettyTable(["serialNumber", "CPU(%)", "user(%)", "kernel(%)", "faults", "timestamp"])
            for i in range(num):
                cpu = self.get_cpu_usage(device_name, app_package)
                result.add_row([i+1, cpu[0], cpu[1], cpu[2], cpu[3], get_current_time()])
                time.sleep(3)  # 每间隔3s获取一次
            print("\nCPU占有率报告:")
            print(result)
        except:
            print("CPU测试失败")


class CPUUsage:
    def __init__(self, *parm):
        self.android = CPUUsageAndroid()
        if parm[0] is None:
            self.num = 1
        else:
            self.num = math.floor(int(parm[0]) / 3)

    def cpu_usage_android(self, app_name, device_name):
        app_info = ReadConfigFile(android_path).get_info('app', app_name)
        device_info = ReadConfigFile(android_path).get_info('device', device_name)
        self.android.cpu_usage_report(device_info['deviceName'], app_info['appPackage'], self.num)
