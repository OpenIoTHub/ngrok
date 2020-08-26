#!/usr/bin/env python
import sys
PYTHON2 = sys.version_info[0] < 3
__version__ = '0.1.6'
def un_zip(file_name,to_path):
    import zipfile
    zip_file = zipfile.ZipFile(file_name)
    for names in zip_file.namelist():
        if not to_path:
            to_path = "./"
        zip_file.extract(names,to_path)
    zip_file.close()

def un_tar_gz(from_path,to_path):
    import tarfile
    tar = tarfile.open(from_path)
    names = tar.getnames()
    for name in names:
        if not to_path:
            to_path = "./"
        tar.extract(name, path=to_path)
    tar.close()

def downloadFile(url,path):
    import os,urllib
    def Schedule(a, b, c):
        per = 100.0 * a * b / c
        if per > 100:
            per = 100
        print('%.2f% %' % per)
    if path is None:
        path = "./"
    filename = url.split("/")[-1]
    local = os.path.join(path,filename)
    urllib.urlretrieve(url,local,Schedule)
    if "tar.gz" in url:
        un_tar_gz(filename,None)
        os.remove(filename)
    else:
        un_zip(filename,None)
        os.remove(filename)

def getJsonObj(url):
    import urllib2,json
    if url is None:
        url = "https://raw.githubusercontent.com/OpenIoTHub/ngrok/master/data.json"
    req = urllib2.Request(url)
    res_data = urllib2.urlopen(req)
    res = res_data.read()
    return json.loads(res)

def pingIP(ip):
    import ping
    result = ping.quiet_ping(ip, timeout=2, count=10, psize=64)
    return result

def portOnLine(address,port):
    import socket
    s = socket.socket()
    s.settimeout(1)
    try:
        s.connect((address, port))
        s.close()
        return True
    except:
        return False

def list():
    print("ngrok versions:")
    jsonObj = getJsonObj(url=None)
    print(jsonObj["github_versions"])


def servers():
    print("lsit servers:")
    jsonObj = getJsonObj(url=None)
    best = {}
    for server in jsonObj["servers"]:
        print("+-------------------------------------------------------+")
        for key in server:
            if isinstance(server[key],bool):
                print(key+":"+str(server[key]).lower())
            else:
                print(key + ":" + str(server[key]))
        ping = pingIP(server["ip_domian"])
        if ping[1]:
            print("ping lost:" + str(ping[0])+"%")
            print("ping max:" + str(int(ping[1])) + "ms")
            print("ping avg:" + str(int(ping[2])) + "ms")
            status = portOnLine(server["ip_domian"], int(server["bind_port"]))
            if status:
                print("ngrok Status:OnLine")
                if best:
                    if best['pingavg'] > int(ping[2]):
                        best = server
                        best['pingavg'] = int(ping[2])
                else:
                    best = server
                    best['pingavg'] = int(ping[2])
            else:
                print("ngrok Status:OffLine")
        else:
            print("ping lost:" + str(ping[0]) + "%")
            print("ngrok Status:OffLine")

    print("+******************recommend host******************+")
    if best:
        for key in best:
            if isinstance(best[key], bool):
                print(key + ":" + str(best[key]).lower())
            else:
                print(key + ":" + str(best[key]))
    else:
        print("+\t\tno online ngrok\t\t\t+")
    print("+***********************end************************+")

def download(version):
    url = ""
    jsonObj = getJsonObj(url=None)
    os_arch_list = jsonObj["os_arch"]
    for oa in range(len(os_arch_list)):
        print(str(oa)+":"+os_arch_list[oa])
    select = input("please input what you want download:")
    print("you selected:"+os_arch_list[select])
    if "windows" in os_arch_list[select]:
        url = "https://github.com/fatedier/frp/releases/download/v%s/frp_%s_%s.zip" % (version, version, os_arch_list[select])
    else:
        url = "https://github.com/fatedier/frp/releases/download/v%s/frp_%s_%s.tar.gz" % (version, version, os_arch_list[select])
    if url:
        print("start download from:"+url)
        downloadFile(url,"./")
        print("download complated!")
def install(path):
    if path:
        print("install")
    else:
        print("install ./")

def pinfo():
    print("""
        =============================
        Ngrok NAT Downloader for Pyhton
        =============================

        pip install ngrok
        ngrok -h
        -----------------------------
        src: https://github.com/OpenIoTHub/ngrok
        -----------------------------
        """)

def main():
    # downloadFile("http://dldir1.qq.com/qqfile/qq/QQ8.9/20026/QQ8.9.exe","./")
    # print(getJsonObj("http://127.0.0.1:8000/ajax/t_erp_aliexpress_online_info_page?perpage=1&page=2"))
    # print(pingIP("www.baidu.com"))
    # print(portOnLine("www.baidu.com",81))
    import argparse
    parser = argparse.ArgumentParser(description='ngrok', prog='ngrok')
    parser.add_argument('--list', '-l', help='list version', action='store_true')
    parser.add_argument('--servers', '-s', help='free servers', action='store_true')
    # parser.add_argument('--path', '-p', help='path')
    parser.add_argument('--download', '-d', help='download program')
    # parser.add_argument('--install', '-i', help='install program')
    args = parser.parse_args()
    print(args)
    if args.list:
        list()
    if args.servers:
        servers()
    if args.download:
        download(args.download)
    # if args.install:
    #     install(args.path)
    if not args.list and not args.servers and not args.download:
        pinfo()

def _main():
    main()
    
if __name__ == '__main__':
    _main()
