# -*- coding: utf-8 -
import os
import json
import time
cur_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
android_path = os.path.join(cur_path, "android.json")
apk_path = os.path.join(cur_path, "apk")
monkey_report_path = os.path.join(cur_path, "monkeyReport")


# 获取当前的时间戳
def get_current_time():
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return current_time


class ReadConfigFile:
    def __init__(self, path):
        self.path = path

    def read_json(self):
        with open(self.path, 'r', encoding='utf-8') as file:
            # 使用load方法将读出的字符串转字典
            content = json.load(file)
            file.close()
        return content

    def get_info(self, *parm):
        android_content = ReadConfigFile(android_path).read_json()['content']
        if parm[0] == 'app':
            for app_info in android_content['app_info']:
                if app_info['name'] == parm[1]:
                    return app_info['info']
        elif parm[0] == 'device':
            for device_info in android_content['device_info']:
                if device_info['name'] == parm[1]:
                    return device_info['info']
        elif parm[0] == 'appium':
            return android_content['appium_info']


class CreateFile:
    def __init__(self, path):
        self.path = path

    def create_folder(self):
        # 如果不存在文件夹，就创建一个
        if not os.path.exists(self.path):
            os.mkdir(self.path)

    def write_json(self, default):
        if not os.path.exists(self.path):
            with open(self.path, 'w', encoding='utf-8') as file:
                json.dump(default, file, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))
            file.close()


android_json_default = {
    "content": {
        "app_info": [
            {"name": "taobao", "info": {"appPackage": "com.taobao.taobao", "appActivity": "com.taobao.tao.Welcome"}},
            {"name": "weixin", "info": {"appPackage": "com.tencent.mm", "appActivity": "com.tencent.mm.ui.LauncherUI"}},
            {"name": "dangdang", "info": {"appPackage": "com.dangdang.buy2", "appActivity": "com.dangdang.buy2.StartupActivity"}}
        ],
        "device_info": [
            {"name": "SamsungGalaxyS6", "info": {"platformVersion": "6.0", "deviceName": "192.168.58.102:5555"}},
            {"name": "SamsungGalaxyS10", "info": {"platformVersion": "9.0", "deviceName": "192.168.58.101:5555"}}],
        "appium_info":
            {"appiumIp": "http://127.0.0.1:4723/wd/hub"}
    },
    "comment": {
        "_comment": "this is comments",
        "jsondata": {
            "app_info": "app信息，app_name要保持与包名称一致，appPackage包名，appActivity程序名",
            "device_info": "移动设备信息，device_name自定义的设备名称（用于区分设备），platformVersion设备安卓版本号,deviceName设备id（通过adb devices获取）",
            "appium_info": "appium服务器信息，appiumIp服务器IP地址（如果使用远程服务器填写对应IP）"
        }
    }
}
# 如果没有android.json,自动创建并写入默认值
CreateFile(android_path).write_json(android_json_default)
# 创建apk文件夹
CreateFile(apk_path).create_folder()

if __name__ == "__main__":
    # 读取android.json信息
    print(ReadConfigFile(android_path).get_info('app', 'taobao'))
    print(ReadConfigFile(android_path).get_info('device', 'Samsung Galaxy S6'))
    print(ReadConfigFile(android_path).get_info('appium'))

