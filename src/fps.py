# -*- coding: utf-8 -
import math
from src import *
from src.shell import *
from prettytable import PrettyTable


class FPSAndroid:

    # adb命令获取APP的fps情况
    def fps(self, device_name, app_package):
        stmt = "adb -s %s shell dumpsys gfxinfo %s" % (device_name, app_package)
        result = subprocess_popen(stmt)
        return result

    def get_fps(self, device_name, app_package):
        res = self.fps(device_name, app_package)
        del res[:res.index("Profile data in ms:")]  # 找到"Profile data in me:"并删除之前的所有多余内容
        # del res[res.index("View hierarchy:"):]  # 找到"View hierarchy:"并删除之后的所有多余内容
        res = [re for re in res if re != ""]  # 去除所有空行
        res = [re.replace("\t", " ").strip(" ") for re in res]  # 去除内容中的所有\t字符
        result = []
        for re in res:
            if re == "Draw Prepare Process Execute":  # 遍历结果找到Draw Prepare Process Execute
                coordinates = res.index("Draw Prepare Process Execute")  # 获取Draw Prepare Process Execute坐标（第一个出现的位置，因为for循环就是按照顺序进行的，可以保证其相互对应）
                if len(res[coordinates+1].split()) == 4:  # 确定找到Draw Prepare Process Execute后，是有fps数据出现的
                    page = res[coordinates-1].split("/")[1]  # 获取fps的页面信息
                    del res[:coordinates+1]  # 从结果中将Draw Prepare Process Execute以及之前的内容删除
                    fps_list = []
                    for r in res:
                        if len(r.split()) == 4:
                            fps_list.append(r.split())  # 循环清理后的res，获取fps列表
                        else:
                            break  # fps列表有4个数据，遍历到不是的时候退出遍历
                    result.append([page, fps_list])  # 结果写入fps的list中
                else:
                    del res[:coordinates+1]  # 此处删除是为了不影响后面页面fps信息的提取
        if result == []:
            # print("未获取到fps数据，请操作应用程序")
            result_list = [["null", "null", "null"]]
            return result_list  # 当APP不操作时是无法获取fps信息的,使用null表示所有值
        else:
            result_list = []
            for res in result:
                page_res = res[0]
                fps_res = res[1]
                frame_count = len(fps_res)  # 获取行数
                jank = 0
                vsync_overtime_sum = 0
                for re in fps_res:
                    render_time = float(re[0]) + float(re[1]) + float(re[2]) + float(re[3])  # 计算一帧所花费的时间
                    if render_time > 16.67:
                        jank += 1  # 如果大于16.67则即为跳针
                        vsync_overtime = math.ceil(render_time / 16.67) - 1  # 计算需要的额外vsync
                        vsync_overtime_sum += vsync_overtime
                jank_percentage = "%.2f%%" % (jank / frame_count * 100)
                fps = "%.1f" % (frame_count * 60 / (frame_count + vsync_overtime_sum))
                result_list.append([page_res, fps, jank_percentage])
            return result_list

    def fps_report(self, device_name, app_package, num):
        try:
            result = PrettyTable(["serialNumber", "page", "FPS", "frameLossRate (%)", "timestamp"])
            for i in range(num):
                fps_list = self.get_fps(device_name, app_package)
                for fps in fps_list:
                    result.add_row([i+1, fps[0], fps[1], fps[2], get_current_time()])
                time.sleep(3)  # 每间隔3s获取一次
            print("\nFPS检测报告：")
            print(result)
        except:
            print("FPS测试失败")


class FPS:
    def __init__(self, *parm):
        self.android = FPSAndroid()
        if parm[0] is None:
            self.num = 1
        else:
            self.num = math.floor(int(parm[0]) / 3)

    def fps_android(self, app_name, device_name):
        app_info = ReadConfigFile(android_path).get_info('app', app_name)
        device_info = ReadConfigFile(android_path).get_info('device', device_name)
        self.android.fps_report(device_info['deviceName'], app_info['appPackage'], self.num)
