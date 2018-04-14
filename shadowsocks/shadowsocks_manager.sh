#!/usr/bin/env python
#coding = utf-8

import urllib2
import json
import os


def get_ip():
    def get_ip_inform(ip):
        apiurl = "http://ip.taobao.com/service/getIpInfo.php?ip=%s" % ip
        content = urllib2.urlopen(apiurl).read()
        data = json.loads(content)['data']
        code = json.loads(content)['code']
        if code == 0:
            print "%s  %s%s%s \n" % (data["ip"].encode('utf-8'), data["country"].encode('utf-8'), data["region"].encode('utf-8'), data["city"].encode('utf-8'))
        else:
            print data.encode('utf-8')

    str = os.popen('netstat -anp|grep python|grep ESTABLISHED').read()
    str_list = []
    for i in str.split('\n'):
        if i != '' and i != ' ':
            i_s = [j for j in i.split(' ') if j !=
                   '' and j != ' '][4].split(':')[-2]
            str_list.append(i_s)
    for i in set(str_list):
        get_ip_inform(i)


def main():
    str = '''
    please select your option
    1 show connectted ip and ip information
    2 chang server config
    3 start server
    4 stop server
    5 restart server
    6 show server status 
    0 quit
    '''
    print str
    number = 0
    while(True):
        try:
            number = int(raw_input("please input [default is 0]: "))
        except ValueError:
            number = 0
        if number == 0:
            exit()
        elif number == 1:
            get_ip()
        elif number == 2:
            print 'vi /etc/shadowsocks.json'
            print 'vi /etc/sysconfig/iptables'
            print 'reboot this machine'
        elif number == 3:
            os.system('/etc/init.d/shadowsocks start')
        elif number == 4:
            os.system('/etc/init.d/shadowsocks stop')
        elif number == 5:
            os.system('/etc/init.d/shadowsocks restart')
        elif number == 6:
            os.system('/etc/init.d/shadowsocks status')


if __name__ == '__main__':
    main()
