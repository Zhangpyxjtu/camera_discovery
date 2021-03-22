#!/usr/bin/env python
# -*- coding: utf-8 -*-
from onvif import ONVIFCamera
import os
import json
import requests
import time
# import sensecam_discovery
import datetime
import zeep
import re
import netifaces
from typing import List
import WSDiscovery
import subprocess


# 获取环境变量
# edgenodeKey = os.environ.get("edgenodeKey")
# user = os.environ.get("user")
# pwd = os.environ.get("pwd")
# url = os.environ.get("url")
# print(edgenodeKey)
# print(user)
# print(pwd)
# print(url)
user = 'admin'
pwd = 'a123456789'
# url = 'http://101.206.211.217:8003/mec/v1/device/edge-endpoint/'
# edgenodeKey = 'dell31312312313'


# 定义变量
headers = {'content-type': "application/json"}


# 后端请求
def backend_req(data):
    response = requests.post(url, data=data, headers=headers)
    curr_time = datetime.datetime.now()
    time_str = datetime.datetime.strftime(curr_time,'%Y-%m-%d %H:%M:%S')
    print(time_str,response.text)
    print(time_str,response.status_code)


def discover(scope = None) -> List:
    """Discover cameras on network using onvif discovery.

    Returns:
        List: List of ips found in network.
    """
    lst = list()
    if(scope == None):
        cmd = 'hostname -I'
        scope = subprocess.check_output(cmd, shell=True).decode('utf-8')
    wsd = WSDiscovery.WSDiscovery()
    wsd.start()
    ret = wsd.searchServices()
    for service in ret:
        get_ip = str(service.getXAddrs())
        get_types = str(service.getTypes())
        for ip_scope in scope.split():
            result = get_ip.find(ip_scope.split('.')[0] + '.' + ip_scope.split('.')[1])
            if result > 0 and get_types.find('onvif') > 0:
            	#下面是更改的代码
                # string_result = get_ip[result:result+13]
                string_result = get_ip[result:].split('/')[0]
                string_result = string_result.split(':')
                string_result = string_result[0]
                # lst = string_result
                # print(string_result)
                lst.append(string_result)
                # if len(string_result)>1:
                #     lst.append([string_result[0],string_result[1]])
                # else:
                #     lst.append([string_result[0]])
    wsd.stop()
    lst.sort()
    return lst

while True:
    # 获取ip
    while True:
        # ips = sensecam_discovery.discover()
        ips = discover()
        curr_time = datetime.datetime.now()
        time_str = datetime.datetime.strftime(curr_time,'%Y-%m-%d %H:%M:%S')
        if not ips:
            print("INFO",time_str,'NO Camera')
        else:
            print("INFO",time_str,"ips: ", ips)
            break

    for ip in ips:
        try:
            cam = ONVIFCamera(ip, 80, user, pwd, './wsdl')
            maun = cam.devicemgmt.GetDeviceInformation()
            #获取视频信息
            id = maun.SerialNumber
            brand = maun.Manufacturer
            device = maun.Model
            print(id,brand,device)

        except Exception as e:
            print(e)
    time.sleep(10)
