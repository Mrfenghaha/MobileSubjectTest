# -*- coding: utf-8 -
from src import *
from src.shell import *
from appium import webdriver


class UninstallAndroid:

    # 使用adb命令卸载安卓APP
    def adb_uninstall(self, device_name, app_package):
        stmt = "adb -s %s uninstall %s" % (device_name, app_package)
        result = subprocess_popen(stmt)
        return result

    # 使用appium卸载安卓APP
    def appium_uninstall(self, apk_path, app_package, app_activity, device_name, platform_version, appium_ip):
        start_info = {
            # 平台名称
            "platformName": 'Android',
            # 平台版本号
            "platformVersion": platform_version,
            # 设备名称
            'deviceName': device_name,
            # app包名
            'appPackage': app_package,
            # app程序名
            'appActivity': app_activity,
            # app文件地址
            'app': apk_path,
            # 是否不每次重新安装
            'noReset': True}
        driver = webdriver.Remote(appium_ip, start_info)
        driver.remove_app(app_package)
        driver.quit()

    def uninstall_report(self, device_name, app_package):
        print("\n卸载报告：")
        result = self.adb_uninstall(device_name, app_package)
        if result is False:
            pass
        elif "DELETE_FAILED_INTERNAL_ERROR" in result[len(result) - 1]:
            print("卸载失败，APP已经不存在\n%s" % get_current_time())
        else:
            print("卸载成功\n%s" % get_current_time())


class Uninstall:

    def __init__(self):
        self.android = UninstallAndroid()

    def uninstall_android(self, app_name, device_name):
        app_info = ReadConfigFile(android_path).get_info('app', app_name)
        device_info = ReadConfigFile(android_path).get_info('device', device_name)
        self.android.uninstall_report(device_info['deviceName'], app_info['appPackage'])
