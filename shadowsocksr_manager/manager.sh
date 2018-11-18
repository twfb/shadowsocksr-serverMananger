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
    current_ports = re.findall('(\d+).+?(\d+)', os.popen('iptables -L INPUT --line-numbers').read())
    def change_port():
        print 'change iptables config file to let port open /n'
        show_port()
        a_or_r = raw_input('add(a), remove(r) or quit(q)  [q]:')
        if a_or_r != 'a' and a_or_r != 'r':
            return
        if a_or_r == 'a':
            print 'please input port'
            print 'for example:\n\t8080,8978'
            ports_list=raw_input('your ports:').replace(' ', '').split(',')
            for port in ports_list:
                os.system('iptables -I INPUT -p tcp --dport {0} -j ACCEPT'.format(port))
        elif a_or_r == 'r':
            for i in current_ports:
                print i[1]
            ports = raw_input('please input the port that you want to remove, such as \'8009,8010\':').replace(' ', '').split(',')
            for i in ports:
                for v in current_ports:
                    if i == v[1]:
                        os.system('iptables -D INPUT {0}'.format(v[0]))

        os.system('service iptables save')
        os.system('/etc/init.d/shadowsocks restart')
        print 'change port success'

    def show_port():
        print '\n   current open port: \n',
        for i in current_ports:
            print '{0}. {1}'.format(i[0], i[1])
            print '\n'

    if raw_input('I just want to change port in iptables rules[N/y]:') == 'y':
        change_port()

    if raw_input('edit config file [N/y]:') == 'y':
        os.system('vi /etc/shadowsocks.json')
        if raw_input('you changed ports [N/y]:') == 'y':
            change_port()
    print 'change success.'
    

def main():
    str='''
    please select your option
    1 show connectted ip and ip information
    2 change server config
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
            os.system('service iptables restart')
            os.system('/etc/init.d/shadowsocks start')
        elif number == 4:
            os.system('/etc/init.d/shadowsocks stop')
        elif number == 5:
            os.system('service iptables restart')
            os.system('/etc/init.d/shadowsocks restart')
        elif number == 6:
            os.system('/etc/init.d/shadowsocks status')


if __name__ == '__main__':
    main()
