#!/usr/bin/env python
# coding = utf-8

import urllib2
import os
import json
import re


def get_ip(is_verbose):
    def get_ip_inform(ip):
        api_url = "http://ip-api.com/json/%s" % ip
        content = urllib2.urlopen(api_url).read()
        json_data = json.loads(content)
        if is_verbose != 'y':
            print '{0}{1} {2} {3}'.format(ip.ljust(20), json_data['country'], json_data['regionName'], json_data['city'].ljust(20))
        else:
            print ip
            for i, v in json_data.items():
                print '\t{0}: {1}'.format(i, v)
            print '\n'
    str=os.popen('netstat -anp|grep python|grep ESTABLISHED').read()
    for i in set(set(re.findall('.+f:(.+):.*ES', str))):
        get_ip_inform(i)

def change_config():
    os.system('vi /etc/shadowsocks.json')
    if raw_input('Do you change your port [N/y]') == 'y':
        print 'please input port'
        print 'for example:\n\t8080,8978'
        ports_list=raw_input('your ports:').replace(' ', '').split(',')
        for port in ports_list:
            os.system(
                'iptables -I INPUT -p tcp --dport {0} -j ACCEPT'.format(port))
    os.system('/etc/init.d/shadowsocks restart')
    print 'change success.'

def main():
    str='''
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
    number=0
    while(True):
        try:
            number=int(raw_input("please input [default is 0]: "))
        except ValueError:
            number=0
        if number == 0:
            exit()
        elif number == 1:
            get_ip(
                raw_input('show verbose information, please input y or n [n]:'))
        elif number == 2:
            change_config()
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
