# -*- coding: utf-8 -
import math
from src import *
from src.shell import *
from prettytable import PrettyTable


class GPUUsageAndroid:

    # adb命令获取GPU信息
    def gpu_info(self, device_name):
        stmt = "adb -s %s shell dumpsys | %s GLES" % (device_name, query)
        result = subprocess_popen(stmt)
        return result

    # adb命令获取GPU使用率
    def gpu_usage(self, device_name):
        stmt = "adb -s %s shell cat /sys/class/kgsl/kgsl-3d0/gpubusy" % (device_name)
        result = subprocess_popen(stmt)
        return result

    def get_gpu_info(self, device_name):
        result = self.gpu_info(device_name)
        gpu_info = result[0].split(":")[1]
        gpu_vendor = gpu_info.split(",")[0].strip(" ")
        return gpu_info, gpu_vendor

    def get_gpu_usage(self, device_name):
        result = self.gpu_usage(device_name)
        gpu = result[0].split()
        if gpu == ["0", "0"]:
            gpu_usage = "0"
        else:
            gpu_usage = "%.2f%%" % (int(gpu[0]) / int(gpu[1]) * 100)
        return gpu_usage

    def gpu_usage_report(self, device_name, num):
        try:
            gpu_info = self.get_gpu_info(device_name)
            if gpu_info[1] != "Qualcomm":
                print("\nGPU使用率报告")
                print("GPU分析仅支持高通")
            else:
                result = PrettyTable(["serialNumber", "GPU(%)", "timestamp"])
                for i in range(num):
                    gpu = self.get_gpu_usage(device_name)
                    result.add_row([i+1, gpu, get_current_time()])
                    time.sleep(3)  # 每间隔3s获取一次
                print("\nGPU使用率报告")
                print(result)
        except:
            print("GPU测试失败")


class GPUUsage:
    def __init__(self, *parm):
        self.android = GPUUsageAndroid()
        if parm[0] is None:
            self.num = 1
        else:
            self.num = math.floor((int(parm[0]) / 3) - 2)

    def gpu_usage_android(self, device_name):
        device_info = ReadConfigFile(android_path).get_info('device', device_name)
        self.android.gpu_usage_report(device_info['deviceName'], self.num)
