# -*- coding: utf-8 -
import argparse
from testcase.installTest import InstallTest
from testcase.monkeyTest import MonkeyTest
from testcase.monitor import Monitor


parser = argparse.ArgumentParser()
parser.add_argument('--platform', '-p', help='平台名称Android或者iOS，必要参数', required=True)
parser.add_argument('--way', '-w', help='APP测试的类型，必要参数', required=True)
parser.add_argument('--app', '-a', help='APP名称(不需要加.apk后缀，也是JSON文件中自定义APP名称)，必要参数', required=True)
parser.add_argument('--device', '-d', help='设备名称（JSON文件中自定义设备名称），必要参数', required=True)
parser.add_argument('--seconds', '-s', help='结果获取时间（秒为单位），非必要参数')
args = parser.parse_args()
if __name__ == "__main__":
    if args.way == "install":
        InstallTest(args.platform).install(args.app, args.device)
    elif args.way == "monitor":
        Monitor(args.platform).monitor(args.app, args.device, args.seconds)
    elif args.way == "installTest":
        InstallTest(args.platform).install_test(args.app, args.device)
    elif args.way == "monkeyTest":
        MonkeyTest(args.platform).monkey_test(args.app, args.device, args.seconds)
