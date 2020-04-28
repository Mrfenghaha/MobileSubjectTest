# -*- coding: utf-8 -
import math
from src import *
from src.shell import *
from prettytable import PrettyTable


class DeviceInfoAndroid:

    # adb命令获取设备型号
    def device_model(self, device_name):
        stmt = "adb -s %s shell getprop ro.product.model" % device_name
        result = subprocess_popen(stmt)
        return result

    # adb命令获取设备系统版本
    def device_system_version(self, device_name):
        stmt = "adb -s %s shell getprop ro.build.version.release" % device_name
        result = subprocess_popen(stmt)
        return result

    # adb命令获取设备GPU信息
    def device_gpu(self, device_name):
        stmt = "adb -s %s shell dumpsys | %s GLES" % (device_name, query)
        result = subprocess_popen(stmt)
        return result

    # adb命令获取设备整体内存
    def device_total_memory(self, device_name):
        stmt = "adb -s %s shell cat /proc/meminfo | %s MemTotal" % (device_name, query)
        result = subprocess_popen(stmt)
        return result

    # adb命令获取设备屏幕参数
    def device_screen_parameters(self, device_name):
        stmt = "adb -s %s shell dumpsys window displays" % device_name
        result = subprocess_popen(stmt)
        return result

    # adb命令获取设备电池状况
    def device_battery(self, device_name):
        stmt = "adb -s %s shell dumpsys battery" % device_name
        result = subprocess_popen(stmt)
        return result

    def get_device_info(self, device_name):
        model = self.device_model(device_name)[0]
        system_version = self.device_system_version(device_name)[0]
        gpu = self.device_gpu(device_name)[0].split(":")[1]
        total_memory = self.device_total_memory(device_name)[0].split(":")[1].strip(" kB")
        screen_parameters = self.device_screen_parameters(device_name)[2]
        screen_resolution = screen_parameters.split()[0].split("=")[1]
        app_resolution = screen_parameters.split()[3].split("=")[1]
        screen_density = screen_parameters.split()[1]
        battery = self.device_battery(device_name)
        for ba in battery:
            if "health:" in ba:
                health = ba.split(":")[1].strip(" ")
                if health == "2":
                    battery_health = "health"
                else:
                    battery_health = "unhealthy"
                break
        return model, system_version, gpu, total_memory, screen_resolution, app_resolution, screen_density, battery_health

    def device_info_report(self, device_name):
        try:
            device_info = self.get_device_info(device_name)
            result = "设备信息\n"
            result += "设备型号：%s\n" % device_info[0]
            result += "系统版本：%s\n" % device_info[1]
            result += "GPU信息：%s\n" % device_info[2]
            result += "设备内存：%sG\n" % "%.2f" % (int(device_info[3])/1024/1024)
            result += "屏幕分辨率：%s\n" % device_info[4]
            result += "应用程序分辨率：%s\n" % device_info[5]
            result += "屏幕密度：%s\n" % device_info[6]
            result += "电池健康情况：%s" % device_info[7]
            print(result)
        except:
            print("设备信息获取失败")


class DeviceInfo:
    def __init__(self):
        self.android = DeviceInfoAndroid()

    def device_info_android(self, device_name):
        device_info = ReadConfigFile(android_path).get_info('device', device_name)
        self.android.device_info_report(device_info['deviceName'])
