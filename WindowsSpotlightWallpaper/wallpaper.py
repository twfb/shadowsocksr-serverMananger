# -*- encoding: utf-8 -*- 
"""
1.安装python2，开启windows聚焦
2.安装PIL库
3.选择或创建一个文件夹作为壁纸存储的地方
4.在设置里选择壁纸存储的文件夹，并在设置中设置为幻灯片
5.解释下 我是将喜欢的壁纸前面加'z'然后手动编号， 不喜欢的也是加‘z’不过后面加99999999999999
6.可以将wallpaper.bat添加到计划任务中具体细节见 http://blog.csdn.net/wuzboy/article/details/51206570
"""
import os
from PIL import Image
from PIL import ImageFile

P_FILE = 'C:\Users\用户名\AppData\Local\Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets'
#windows焦点图片默认存储位置，需要将“用户名”更换为你的用户名

global path
path = 'D:\\Picture\\Themes' #存储壁纸的文件夹，注意运行该程序后将会删除没有以z开头的    所有文件


ImageFile.LOAD_TRUNCATED_IMAGES = True

def equal(img_file1, img_file2): 
    if img_file1 == img_file2:
        return True
    fp1 = open(img_file1,'rb')
    fp2 = open(img_file2, 'rb')
    img1 = Image.open(fp1)
    img2 = Image.open(fp2)
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    b =  img1 == img2
    fp1.close()
    fp2.close()
    return b
    

def move():
    os.chdir(path)
    os.system('ren *.jpg *.')
    for root, dirs, files in os.walk(path):
        for fileName in files:
                if fileName[0:1]!='z':
                    os.remove(fileName)
    os.system(r'xcopy /y {} {}'.format(P_FILE, path ))
    print('move successed')


def identify():    
    li = []
    for root, dirs, files in os.walk(path):
        for i, fileName1 in enumerate(files):
            if fileName1[0]!='z':
                    try:
                        fp1 = open(fileName1,'rb')
                        img1 = Image.open(fp1)
                        x, y = img1.size
                        if fp1:
                            fp1.close()
                        if x != 1920 or y != 1080:
                            li.append(fileName1)
                            continue
                        else:
                            for fileName2 in files[i+1:][::-1]:
                                if fileName2[0]=='z':
                                    if equal(fileName1, fileName2):
                                        li.append(fileName1)
                                        break

                    except IOError:
                        if fp1:
                            fp1.close()
                        if fileName1:
                            li.append(fileName1)
    print('identify successed')
    return li



def del_fun(li):
    for i in li:
        try:
            os.remove(i)
        except Exception:
            pass
    
os.chdir(path)
move()
del_fun(identify())
os.system('ren *.* *.jpg')
print('THE END')
