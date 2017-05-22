# -*- encoding: utf-8 -*- 
import os
from PIL import Image
from PIL import ImageFile

def equal(im1, im2): 
    """
    if same return Ture else return False
    """
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    return im1 == im2

ImageFile.LOAD_TRUNCATED_IMAGES = True
global path
path = 'F:\\Picture\\Themes'  #存储壁纸的文件夹
       


def move():
    os.chdir(path)
    os.system('ren *.jpg *.')
    for root, dirs, files in os.walk(path):
        for fileName in files:
                if fileName[0:1]!='z':
                    os.remove(fileName)
    os.system(r'xcopy /y C:\Users\用户名\AppData\Local\Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets F:\Picture\Themes')
                                     #windows焦点图片默认存储位置，需要将“用户名”更换为你的用户名                                                                                         #存储壁纸的文件夹
    print('move successed')


def identify():    
    for root, dirs, files in os.walk(path):
        for fileName1 in files:
                if fileName1[0]!='z':
                    try:
                        fp1 = open(fileName1,'rb')
                        fp2 =open( fileName1, 'rb')
                        img1 = Image.open(fp1)
                        x, y = img1.size
                        if x != 1920 or y != 1080:
                            c = 1/0
                        else:
                            for root2, dirs2, files2 in os.walk(path):
                                for fileName2 in files2:
                                    if fileName2[0]=='z':
                                        fp2 =open( fileName2, 'rb')
                                        img2 = Image.open(fp2)
                                        if img1 == img2:
                                            c = 1/0
                    except IOError:
                        fp1.close()
                        fp2.close()
                        if fileName1:
                            os.remove(fileName1)
                        continue
                    except ZeroDivisionError:
                        fp1.close()
                        fp2.close()
                        if fileName1:
                            os.remove(fileName1)
                        continue
    print('identify successed')

os.chdir(path)
move()
identify()
os.system('ren *.* *.jpg')
print('THE END')
