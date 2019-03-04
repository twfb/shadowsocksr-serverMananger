# -*- coding:utf-8 -*-
import urllib.request as urllib2
import re
from optparse import OptionParser
import threading
import queue
import os
import sys
import platform
import zipfile
import os
import time


def is_windows_system():
    return 'Windows' in platform.system()


def is_linux_system():
    return 'Linux' in platform.system()


def del_dir(dir_name):
    a = input('I will delete {}? y/n [y]'.format(sys.path[0] + '\\' + dir_name))
    if a == 'y' or a == '':
        if is_windows_system():
            os.popen('rd /s /q ' + dir_name)
        else:
            os.popen('rm -rf' + dir_name)
    else:
        sys.exit(0)


def get_page(url_list):
    user_agent = r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'
    headers = {'User-Agent': user_agent}
    q = queue.Queue()

    def get_p(url):
        request = urllib2.Request(url, headers=headers)
        response = urllib2.urlopen(request)
        q.put(str(response.read()))

    threads = []

    for i in url_list:
        t = threading.Thread(target=get_p, args=(i,))
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    page_list = []

    while not q.empty():
        page_list.append(q.get())

    return page_list


def get_url(home_url, page_num, tab_num):
    tab = ['stars', 'repositories']
    return home_url + '?page={}&tab={}'.format(page_num, tab[tab_num])


def get_repo(home_url, tab_num):
    max_num = 1
    first_start_page = get_page([get_url(home_url, 1, tab_num)])[0]
    pattern = [r'.*>(\d+)<.*"next_page".*?',
               r'.*>(\d+)<.*next_page.*']
    ma = re.match(pattern[tab_num], first_start_page)

    if ma is not None:
        max_num = int(ma.group(1))

    url_list = []
    for i in range(1, max_num + 1):
        url_list.append(get_url(home_url, i, tab_num))

    pattern = [r'd-inline-block mb-1.*?href="(.*?)"', r'<h3>.*?href="(.*?)".*?codeRepository']
    project_list = []

    for i in get_page(url_list):
        project_list += re.findall(pattern[tab_num], i)

    return project_list


def download(project_list, directory):
    threads = []

    for i in project_list:
        pattern = r'/(.+)/(.+$)'
        ma = re.match(pattern, i)
        if os.path.exists(directory + '/' + i):
            del_dir(directory + '\\' + ma.group(1) + '\\' + ma.group(2))
            time.sleep(0.1)

    for i in project_list:
        print('downloading ' + i[1:] + ' to ' + directory + '/')
        repo_url = 'https:://github.com' + i
        t = threading.Thread(target=git_clone, args=(i, directory + i))
        threads.append(t)

    print('downloading please don\'t stop it')

    for t in threads:
        t.start()


def git_clone(name, path):
    username, projectname = re.match(
        '(.+)/(.+)', name).groups()
    zipfile_name = projectname + '.zip'
    url = 'https://codeload.github.com/{}/{}/zip/master'.format(
        username, projectname)
    data = request.urlopen(url)
    with open(path+'/'+zipfile_name, 'wb') as f:
        f.write(data.read())
    with zipfile.ZipFile(zipfile_name, 'r') as sqlfile:
        sqlfile.extractall('./{}'.format(projectname))
    os.remove(path+'/'+zipfile_name)


def main():
    parse = OptionParser()
    parse.add_option('-u', '--username',
                     dest='user_name',
                     help='destination\'s github username or link')

    parse.add_option('-t', '--tab',
                     dest='tab',
                     help='download starts(s) or repositories(r) or all(a). default: repositories')

    parse.add_option('-o', '--output', action='store',
                     dest='directory',
                     help='output directory. default: ./Github')

    (option, arges) = parse.parse_args()

    user_name = None
    tab_num = 1
    director = 'GitHub'
    repo_list = []

    if option.user_name is None:
        print('please input username')
        os._exit(1)

    pattern = '(.*?github.com/(.*)\?.*)|(.*?[^com]$)'
    ma = re.match(pattern, option.user_name)
    for u in ma.groups():
        if u:
            user_name = u.strip()
            break

    if option.tab:
        tab = option.tab[0]
        if tab == 's' or tab == 'S':
            tab_num = 0
        elif tab == 'r' or tab == 'R':
            tab_num = 1
        elif tab == 'a' or tab == 'A':
            tab_num = 2

    home_url = 'https://github.com/{}/'.format(user_name)
    if tab_num == 2:
        repo_list += get_repo(home_url, 1)
        repo_list += get_repo(home_url, 0)
    else:
        repo_list = get_repo(home_url, tab_num)

    if option.directory:
        director = option.directory

    download(repo_list, director)


if __name__ == '__main__':
    main()
