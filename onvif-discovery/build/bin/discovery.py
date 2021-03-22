#from camera_discovery import CameraDiscovery
from onvif import ONVIFCamera
# import sensecam_discovery
import datetime
import zeep
import re
import netifaces
from typing import List

# from wsdiscovery.discovery import ThreadedWSDiscovery as WSDiscovery
import WSDiscovery
import subprocess
user = 'admin'
pwd = 'a123456789'

# def discover(scope = None) -> List:
#     """Discover cameras on network using onvif discovery.
#     Returns:
#         List: List of ips found in network.
#     """
#     # Get the scopes from the IPs returned by the bash command `hostname -I`.
#     ips = list()
#     if (scope == None):
#         cmd = 'hostname -I'
#         for iface in netifaces.interfaces():
#             if(netifaces.AF_INET in netifaces.ifaddresses(iface)):
#                 ips.append(netifaces.ifaddresses(iface)[netifaces.AF_INET][0]['addr'])
#         scope = ['.'.join(ip.split('.')[:2]) for ip in ips]
#     # Run WSDiscovery to search the IP from the cameras.
#     wsd = WSDiscovery()
#     wsd.start()
#     ret = wsd.searchServices()
#     # Get just the services from onvif cameras.
#     onvif_services = [s for s in ret if str(s.getTypes()).find('onvif') >= 0]
#     # Extract the IPs of the onvif cameras.
#     urls = [ip for s in onvif_services for ip in s.getXAddrs()]
#     ips = [ip for url in urls for ip in re.findall(r'\d+\.\d+\.\d+\.\d+', url)]
#     # Return a list with the IPs that correspond to the scope.
#     lst = [ip for ip in ips if any(ip.startswith(sp) for sp in scope)]
#     wsd.stop()
#     return sorted(lst)
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
    curr_time = datetime.datetime.now()
    time_str = datetime.datetime.strftime(curr_time,'%Y-%m-%d %H:%M:%S')
    ips = discover()
    print('INFO',time_str,"ip: ",ips)
    print(ips[0])
    # ip = sensecam_discovery.discover()
    # print('INFO',time_str,"ip: ", ip)
    if not ips:
        print('INFO',time_str,'NO Camera')
    else:
        cam = ONVIFCamera(ips[0], 80, user, pwd, './wsdl')
        maun = cam.devicemgmt.GetDeviceInformation()
        print(maun.SerialNumber)
        # pass

