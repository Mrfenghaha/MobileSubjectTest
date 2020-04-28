# -*- coding: utf-8 -
from src import *
from src.shell import *
from appium import webdriver


class InstallAndroid:

    # 使用adb命令安装安卓APP
    def adb_install(self, device_name, apk_path):
        stmt = "adb -s %s install %s" % (device_name, apk_path)
        result = subprocess_popen(stmt)
        return result

    # 使用appium安装安卓APP
    def appium_install(self, apk_path, device_name, platform_version, appium_ip):
        start_info = {
            # 平台名称
            "platformName": 'Android',
            # 平台版本号
            "platformVersion": platform_version,
            # 设备名称
            'deviceName': device_name,
            # app文件地址
            'app': apk_path,
            # 是否不每次重新安装
            'noReset': False}
        driver = webdriver.Remote(appium_ip, start_info)
        driver.quit()

    def install_report(self, device_name, apk_path):
        print("\n安装报告：")
        result = self.adb_install(device_name, apk_path)
        if result is False:
            pass
        elif "Failure" in result[len(result)-1]:
            failure = result[len(result)-1].split("[")[1].split("]")[0]
            print("安装失败  %s\n%s" % (failure, get_current_time()))
        else:
            print("安装成功\n%s" % get_current_time())


class Install:

    def __init__(self):
        self.android = InstallAndroid()

    def install_android(self, app_name, device_name):
        apk_path = os.path.join(cur_path, 'apk/%s.apk' % app_name)
        device_info = ReadConfigFile(android_path).get_info('device', device_name)
        self.android.install_report(device_info['deviceName'], apk_path)
