# -*- coding: utf-8 -
from src import *
from src.shell import *
from prettytable import PrettyTable


class ElectricityUsageAndroid:

    # 获取应用uid
    def get_uid(self, device_name, app_package):
        # 获取线程uid
        stmt = "adb -s %s shell ps | %s %s" % (device_name, query, app_package)
        result = subprocess_popen(stmt)
        uid = result[0].split()[0]
        return uid.replace("_", "")

    # 重置设备耗电量数据
    def electricity_reset(self, device_name):
        stmt = "adb -s %s shell dumpsys batterystats --reset" % device_name
        result = subprocess_popen(stmt)
        return result

    # 设置断开充电
    def electricity_disconnect_charging(self, device_name):
        stmt = "adb -s %s shell dumpsys battery unplug" % device_name
        result = subprocess_popen(stmt)
        return result

    # 恢复设备电池状态
    def electricity_restore(self, device_name):
        stmt = "adb -s %s shell dumpsys battery reset" % device_name
        result = subprocess_popen(stmt)
        return result

    # adb命令查看耗电信息
    def electricity_usage(self, device_name, app_package, uid):
        stmt = "adb -s %s shell dumpsys batterystats %s | %s %s" % (device_name, app_package, query, uid)
        result = subprocess_popen(stmt)
        return result

    def get_electricity_usage(self, device_name, app_package, uid):
        result = self.electricity_usage(device_name, app_package, uid)
        electricity = result[0].split(":")[1].split("(")[0].strip(" ")
        electricity_details = result[0].split("( ")[1].split(" )")[0]
        return electricity, electricity_details

    # n秒内获取耗电量
    def electricity_usage_report(self, device_name, app_package, seconds):
        try:
            uid = self.get_uid(device_name, app_package)
            self.electricity_reset(device_name)
            self.electricity_disconnect_charging(device_name)
            time.sleep(seconds)
            self.electricity_restore(device_name)
            electricity = self.get_electricity_usage(device_name, app_package, uid)
            print("电量使用报告:")
            print("共耗电%smA，详细耗电情况为 %s" % (electricity[0], electricity[1]))
        except:
            print("电量测试失败")

    # 每10秒重置一次并获取耗电量
    def electricity_usage_report2(self, device_name, app_package, num):
        try:
            print("\n电量使用报告:")
            result = PrettyTable(["serialNumber", "electricity(mA)", "electricity_details(mA)", "timestamp"])
            for i in range(num):
                uid = self.get_uid(device_name, app_package)
                self.electricity_reset(device_name)
                self.electricity_disconnect_charging(device_name)
                time.sleep(10)
                self.electricity_restore(device_name)
                electricity = self.get_electricity_usage(device_name, app_package, uid)
                result.add_row([i+1, electricity[0], electricity[1], get_current_time()])
            print(result)
        except:
            print("测试失败")


class ElectricityUsage:
    def __init__(self, *parm):
        self.android = ElectricityUsageAndroid()
        if parm[0] is None:
            self.num = 20
        else:
            self.num = int(parm[0])

    def electricity_usage_android(self, app_name, device_name):
        app_info = ReadConfigFile(android_path).get_info('app', app_name)
        device_info = ReadConfigFile(android_path).get_info('device', device_name)
        self.android.electricity_usage_report(device_info['deviceName'], app_info['appPackage'], self.num)
