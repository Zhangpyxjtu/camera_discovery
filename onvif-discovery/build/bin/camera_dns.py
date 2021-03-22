#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import requests
import time
# import sensecam_discovery
import datetime
import re
import subprocess as sp


# 获取环境变量
edgenodeKey = os.environ.get("edgenodeKey")
url = os.environ.get("url")
# url="http://101.206.211.217:8003/mec/v1/device/edge-endpoint/"
# edgenodeKey = 'dell31312312313'
print(edgenodeKey)
print(url)

# 定义变量
headers = {'content-type': "application/json"}


# 后端请求
def backend_req(data):
    response = requests.post(url, data=data, headers=headers)
    curr_time = datetime.datetime.now()
    time_str = datetime.datetime.strftime(curr_time,'%Y-%m-%d %H:%M:%S')
    print(time_str,response.text)
    print(time_str,response.status_code)

command_srevice = ['systemctl status avahi-daemon.service']
p1 = sp.Popen(command_srevice,shell = True)

while True:
    # 获取ip
    while True:
        command = ['timeout -s SIGKILL 5 avahi-browse -a --resolve']
        p = sp.Popen(command,  shell=True,stdout=sp.PIPE)
        str1 = 'hostname'
        str2 = 'address'
        list_address = []
        list_num = []
        list_ip = []
        for line in p.stdout.readlines():
            line = bytes.decode(line)
            # print(line)
            if (str1 in line):
                address = line[15:-2]
                # print(address,type(address),type(list_address))
                list_address.append(address)
                # print(list_address)
                num = line[15:-8]
                # print(num,type(num),type(list_num))
                list_num.append(num)
                # print(list_num)
            if (str2 in line):
                ip = line[14:-2]
                list_ip.append(ip)
                # print(ip)
        rtsp = list(set(list_address))
        rtsp.sort(key=list_address.index)
        SerialNumber = list(set(list_num))
        SerialNumber.sort(key = list_num.index)
        ips = list(set(list_ip))
        ips.sort(key = list_ip.index)
        curr_time = datetime.datetime.now()
        time_str = datetime.datetime.strftime(curr_time,'%Y-%m-%d %H:%M:%S')
        if not ips:
            print("INFO",time_str,'NO Camera')
        else:
            print("INFO",time_str,"ips: ", ips)
            break
    i = 0        
    for ip in ips:
        try:
            keyval = {'IP': ip,'SerialNumber':SerialNumber[i]}
            loadvariable = json.dumps(keyval)
            # 定义请求字典
            req = {}
            req['edgeNodeKey'] = edgenodeKey
            req['edgeEndpointKey'] = SerialNumber[i]
            req['agreement'] = 'mDNS'
            req['deviceType'] = '摄像头'
            req['deviceTypeDict'] = 1
            req['brand'] = 'None'
            req['uploadVariable'] = loadvariable
            data = json.dumps(req)
            backend_req(data)
        except Exception as e:
            print(e)
        i=i+1
        # print(i)
    time.sleep(10)
