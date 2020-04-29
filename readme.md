## 介绍
本项目为移动端APP的专项测试，目前仅支持Android（使用adb）
实现安装测试、卸载测试、冷/热启动测试，以及信息收集：设备信息、CPU、电量、流量、FPS、GPU、内存、电池温度

## android.json文件、apk文件
* 将需要的APP的apk安装包放在apk文件下
* 修改android.json文件，根据模版添加/修改设备信息、APP信息（APP名称要与apk包名称保持一致，不需要含.apk）

## 环境安装
* 本项目需要python3环境，安装请自行百度
* 安装python库  pip3 install -r requirements.txt

## 测试执行说明
main.py脚本为测试执行统一入口

**查看帮助--help**
```
python3 main.py --help
usage: main.py [-h] --platform PLATFORM --way WAY --app APP --device DEVICE
               [--seconds SECONDS]

optional arguments:
  -h, --help            show this help message and exit
  --platform PLATFORM, -p PLATFORM
                        平台名称Android或者iOS，必要参数
  --way WAY, -w WAY     APP测试的类型，必要参数
  --app APP, -a APP     APP名称(不需要加.apk后缀，也是JSON文件中自定义APP名称)，必要参数
  --device DEVICE, -d DEVICE
                        设备名称（JSON文件中自定义设备名称），必要参数
  --seconds SECONDS, -s SECONDS
                        结果获取时间（秒为单位），非必要参数
```

```
 python3 main.py -p android -w install -a taobao -d Redmi4   # 使用Redmi4手机，安装taobao
 python3 main.py -p android -w installTest -a taobao -d Redmi4  # 使用Redmi4手机，进行taobao的安装、卸载、冷/热启动测试
 python3 main.py -p android -w monkeyTest -a taobao -d Redmi4 -s 60  # 使用Redmi4手机，进行taobao的时常60s的monkey测试，并监控设备资源
 python3 main.py -p android -w monitor -a taobao -d Redmi4 -s 60  # 使用Redmi4手机，进行taobao的时常60s的设备资源监控（用于手动操作设备）
```
## 其他
* monkey测试会输出测试报告在monkeyReport文件夹内，错误信息在error.txt，正确信息在info.txt中
* 测试以及监控的报告见[参考](https://github.com/fengyibo963/MobileSubjectTest/tree/master/monkeyReport/20200428175822.txt)