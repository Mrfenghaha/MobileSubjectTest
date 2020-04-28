# -*- coding: utf-8 -
from src.deviceInfo import DeviceInfo
from src.install import Install
from src.start import Start
from src.uninstall import Uninstall


class InstallTest:
    def __init__(self, platform):
        self.platform = platform.lower()

    def install(self, app_name, device_name):
        if self.platform == "android":
            Install().install_android(app_name, device_name)
        else:
            print("暂不支持ios")

    def uninstall(self, app_name, device_name):
        if self.platform == "android":
            Uninstall().uninstall_android(app_name, device_name)
        else:
            print("暂不支持ios")

    def install_test(self, app_name, device_name):
        if self.platform == "android":
            DeviceInfo().device_info_android(device_name)
            Uninstall().uninstall_android(app_name, device_name)  # 预防设备已经有存在测试APP旧版本，先卸载APP
            print("该次卸载结果不计入整体报告")
            Install().install_android(app_name, device_name)
            Start(2).start(app_name, device_name)
            Uninstall().uninstall_android(app_name, device_name)
        else:
            print("暂不支持ios")
