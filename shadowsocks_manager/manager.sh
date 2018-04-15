#!/usr/bin/env python
#coding = utf-8

import urllib2
import os
import json
import re
# set allow ip in allow_ip_list, for example: allow_ip_list = ['192.168.111.1', '12.167.2.1']
allow_ip_list = ['112.38.217.35', '223, 104.186.2']


def get_ip(is_verbose):
    def get_ip_inform(ip):
        api_url = "http://ip-api.com/json/%s" % ip
        content = urllib2.urlopen(api_url).read()
        json_data = json.loads(content)
        if is_verbose != 'y':
            print '{0}{1} {2} {3}{4}'.format(ip.ljust(20), json_data['country'], json_data['regionName'], json_data['city'].ljust(20), ip in allow_ip_list)
        else:
            print ip
            print '\tallow: {0}'.format(ip in allow_ip_list)
            for i, v in json_data.items():
                print '\t{0}: {1}'.format(i, v)
            print '\n'
    str = os.popen('netstat -anp|grep python|grep ESTABLISHED').read()
    for i in set(set(re.findall('.+f:(.+):.*ES', str))):
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
            if not allow_ip_list:
                print 'recommand set allow ip in this file'
            get_ip(
                raw_input('show verbose information, please input y or n [n]:'))
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
