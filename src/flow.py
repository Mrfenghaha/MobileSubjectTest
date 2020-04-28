# -*- coding: utf-8 -
import math
from src import *
from src.shell import *
from prettytable import PrettyTable


class FlowUsageAndroid:

    def get_uid(self, device_name, app_package):
        # 获取线程pid
        stmt = "adb -s %s shell ps | %s %s" % (device_name, query, app_package)
        result = subprocess_popen(stmt)
        pid = result[0].split()[1]
        # 获取用户Uid
        stmt = "adb -s %s shell cat /proc/%s/status | %s Uid" % (device_name, pid, query)
        result = subprocess_popen(stmt)
        uid = result[0].split()[1]
        return pid, uid

    # adb命令获取APP的流量使用情况-接收数据大小
    def flow_rcv_usage(self, device_name, uid):
        stmt = "adb -s %s shell cat /proc/uid_stat/%s/tcp_rcv" % (device_name, uid)
        result = subprocess_popen(stmt)
        return result

    # adb命令获取APP的流量使用情况-发送数据大小
    def flow_snd_usage(self, device_name, uid):
        stmt = "adb -s %s shell cat /proc/uid_stat/%s/tcp_snd" % (device_name, uid)
        result = subprocess_popen(stmt)
        return result

    def get_flow_rcv_usage(self, device_name, uid):
        result = self.flow_rcv_usage(device_name, uid)
        flow_rcv = result[0].strip(" ")
        return flow_rcv

    def get_flow_snd_usage(self, device_name, uid):
        result = self.flow_snd_usage(device_name, uid)
        flow_rcv = result[0].strip(" ")
        return flow_rcv

    def flow_usage_report(self, device_name, app_package, num):
        try:
            uid = self.get_uid(device_name, app_package)[1]
            result = PrettyTable(["serialNumber", "send(kb)", "sendTotal(kb)", "receive(kb)", "receiveTotal(kb)", "timestamp"])
            receive_total = self.get_flow_rcv_usage(device_name, uid)
            send_total = self.get_flow_snd_usage(device_name, uid)
            receive_change_list = [0]
            send_change_list = [0]
            for i in range(num):
                time.sleep(3)
                receive_total_new = self.get_flow_rcv_usage(device_name, uid)  # 获取3s后的接收新数据
                receive = int(receive_total_new) - int(receive_total)  # 获取初始至当前的数据差
                receive_change_list.append(receive)
                receive_change = receive_change_list[len(receive_change_list)-1] - receive_change_list[len(receive_change_list)-2]  # 获取接收数据与上一个结果的差值

                send_total_new = self.get_flow_snd_usage(device_name, uid)
                send = int(send_total_new) - int(send_total)
                send_change_list.append(send)
                send_change = send_change_list[len(send_change_list)-1] - send_change_list[len(send_change_list)-2]
                del receive_change_list[0]  # 删除前一个数据，保留新数据，用于下次计算
                del send_change_list[0]
                result.add_row([i+1, send_change, send, receive_change, receive, get_current_time()])
            print("\n流量使用报告:")
            print(result)
        except:
            print("流量测试失败")


class FlowUsage:
    def __init__(self, *parm):
        self.android = FlowUsageAndroid()
        if parm[0] is None:
            self.num = 1
        else:
            self.num = math.floor(int(parm[0]) / 3)

    def flow_usage_android(self, app_name, device_name):
        app_info = ReadConfigFile(android_path).get_info('app', app_name)
        device_info = ReadConfigFile(android_path).get_info('device', device_name)
        self.android.flow_usage_report(device_info['deviceName'], app_info['appPackage'], self.num)
