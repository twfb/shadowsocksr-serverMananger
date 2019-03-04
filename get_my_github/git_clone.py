import zipfile
from urllib import request
import os
import re


def git_clone(git_url):
    username, projectname = re.match(
        'https://github.com/(.+)/(.+)', git_url).groups()
    zipfile_name = projectname + '.zip'
    
    url = 'https://codeload.github.com/{}/{}/zip/master'.format(
        username, projectname)
    data = request.urlopen(url)

    with open(zipfile_name, 'wb') as f:
        f.write(data.read())
    with zipfile.ZipFile(zipfile_name, 'r') as sqlfile:
        sqlfile.extractall('.')
    os.rename(projectname+'-master', projectname)
    os.remove(zipfile_name)

git_clone('https://github.com/dhgdhg/py_tools')
