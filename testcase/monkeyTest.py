# -*- coding: utf-8 -
import time
import threading
from src.deviceInfo import DeviceInfo
from src.install import Install
from src.monkey import Monkey
from src.cpu import CPUUsage
from src.gpu import GPUUsage
from src.memory import MemoryUsage
from src.flow import FlowUsage
from src.electricity import ElectricityUsage
from src.temperature import Temperature
from src.fps import FPS


class MonkeyTest:
    def __init__(self, platform):
        self.platform = platform.lower()

    def monkey_test(self, app_name, device_name, seconds):
        if self.platform == "android":
            DeviceInfo().device_info_android(device_name)
            Install().install_android(app_name, device_name)  # 预防设备没有安装测试APP，先安装APP
            print("该次安装结果不计入整体报告")

            threads = []
            t1 = threading.Thread(target=Monkey(seconds).monkey, args=(app_name, device_name))
            threads.append(t1)
            t2 = threading.Thread(target=CPUUsage(seconds).cpu_usage_android, args=(app_name, device_name))
            threads.append(t2)
            t3 = threading.Thread(target=GPUUsage(seconds).gpu_usage_android, args=(device_name,))
            threads.append(t3)
            t4 = threading.Thread(target=MemoryUsage(seconds).memory_usage_android, args=(app_name, device_name))
            threads.append(t4)
            t5 = threading.Thread(target=FlowUsage(seconds).flow_usage_android, args=(app_name, device_name))
            threads.append(t5)
            t6 = threading.Thread(target=ElectricityUsage(seconds).electricity_usage_android, args=(app_name, device_name))
            threads.append(t6)
            t7 = threading.Thread(target=Temperature(seconds).temperature_android, args=(device_name,))
            threads.append(t7)
            t8 = threading.Thread(target=FPS(seconds).fps_android, args=(app_name, device_name))
            threads.append(t8)
            for t in threads:
                # t.setDaemon(True)
                t.start()
                time.sleep(0.25)  # 每个命令间隔0.25s以防结果输出掺杂
        else:
            print("暂不支持ios")
