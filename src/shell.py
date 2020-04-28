# -*- coding: utf-8 -
import os
import sys
import time
import subprocess

# 由于windows的命令行中查找为findstr，liunx和mac是grep
if sys.platform in ['win32', 'win64']:
    query = "findstr"
else:
    query = "grep"


# 只能判断是否执行成功
def os_system(stmt):
    result = os.system(stmt)
    if result is not 0:  # 结果为0则表示执行成功，为其他值则表示执行不成功
        print("命令执行失败，请检查设备连接状态")
    else:
        return result


# 只能获取执行结果
def os_popen(stmt, *parm):
    re = os.popen(stmt).readlines()
    result = []
    for i in range(0, len(re) - 1):  # 由于原始结果需要转换编码，所以循环转为utf8编码并且去除\n换行
        res = re[i].strip('\n')
        result.append(res)
    if parm == ():
        return result  # 获取全部执行结果
    else:
        line = int(parm[0]) - 1
        return result[line]  # 获取执行结果的指定行


# 只能判断是否执行成功
def subprocess_call(stmt):
    result = subprocess.call(stmt)
    # 执行失败不需要特殊处理，命令执行失败会直接报错
    return result  # 结果为0则表示执行成功，为其他值则表示执行不成功


# 只能判断是否执行成功
def subprocess_check_call(stmt):  # 基本与call一致
    result = subprocess.check_call(stmt)
    # 执行失败不需要特殊处理，命令执行失败会直接报错
    return result  # 结果为0则表示执行成功，为其他值则表示执行不成功


# 只能获取执行结果
def subprocess_getoutput(stmt):
    result = subprocess.getoutput(stmt)
    # 执行失败不需要特殊处理，因为该方法无法判断失败成功，只负责将结果进行返回
    return result  # 返回执行结果，但是结果返回的是一个str字符串（不论有多少行）


# 只能获取执行结果
def subprocess_check_output(stmt):
    result = subprocess.check_output(stmt).decode('utf-8')
    # 执行失败不需要特殊处理，命令执行失败会直接报错
    return result  # 返回执行结果，但是结果返回的是一个str字符串（不论有多少行），并且返回的结果需要转换编码


# 既可以判断执行是否成功，还可以获取执行结果
def subprocess_popen(statement):
    p = subprocess.Popen(statement, shell=True, stdout=subprocess.PIPE)  # 执行shell语句并定义输出格式
    while p.poll() is None:  # 判断进程是否结束（Popen.poll()用于检查子进程（命令）是否已经执行结束，没结束返回None，结束后返回状态码）
        if p.wait(timeout=None) is not 0:  # 判断是否执行成功（Popen.wait()等待子进程结束，并返回状态码；如果设置并且在timeout指定的秒数之后进程还没有结束，将会抛出一个TimeoutExpired异常。）
            print("命令执行失败，请检查设备连接状态")
            return False
        else:
            re = p.stdout.readlines()  # 获取原始执行结果
            result = []
            for i in range(len(re)):  # 由于原始结果需要转换编码，所以循环转为utf8编码并且去除\n换行
                res = re[i].decode('utf-8').strip('\r\n')
                result.append(res)
            return result


if __name__ == "__main__":
    stmt = "lss"
    os_system(stmt)
    os_popen(stmt)
    subprocess_call(stmt)
    subprocess_check_call(stmt)
    subprocess_getoutput(stmt)
    subprocess_check_output(stmt)
    subprocess_popen(stmt)
