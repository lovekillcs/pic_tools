import sys
import os
from PIL import Image


class Load_Corpus_with_Iteration(object):
    def __init__(self, path):
        self.path = path

    def __iter__(self):
        for line in open(self.path):
            yield line.split()

# corpus = Load_Corpus_with_Iteration(path)
#     for item in corpus:
#         print item


class PicData:
    pass


allfile = []


def getallfile(path):
    allfilelist = os.listdir(path)
    for file in allfilelist:
        filepath = os.path.join(path, file)
        if os.path.isdir(filepath):
            getallfile(filepath)
        allfile.append(filepath)
    return allfile


def loadFiles(path):
    files = getallfile(path)
    for f in files:
        if '.txt' in f:
            picPath = f.replace('txt', 'png')
            if os.path.isfile(picPath):
                savePath = f.replace('.txt', '/')
                if not os.path.exists(savePath):
                    os.makedirs(savePath)
                print picPath
                img = Image.open(picPath)
                datas = analyzeMeta(f)
                for data in datas:
                    cutPic(img,
                        data.x, data.y, data.width, data.height,
                        data.paddingLeft,
                        data.paddingTop,
                        data.paddingLeft + data.paddingRight + data.width,
                        data.paddingTop + data.paddingBottom + data.height,
                        savePath+data.name+'.png')


def analyzeMeta(path):
    picDatas = []
    with open(path, 'rb') as file:
        for line in file:
            # vaule = 0
            if '=' in line:
                vaule = line.split('=')[1]
            if 'Generic Mono data' in line:
                data = PicData()
                picDatas.append(data)
            elif 'string name =' in line:
                data.name = str(vaule.replace('\"', '').replace(
                    ' ', '').replace('\r\n', ''))
            elif 'int x =' in line:
                data.x = int(vaule)
            elif 'int y =' in line:
                data.y = int(vaule)
            elif 'int width =' in line:
                data.width = int(vaule)
            elif 'int height =' in line:
                data.height = int(vaule)
            elif 'int borderLeft =' in line:
                data.borderLeft = int(vaule)
            elif 'int borderRight =' in line:
                data.borderRight = int(vaule)
            elif 'int borderTop =' in line:
                data.borderTop = int(vaule)
            elif 'int borderBottom =' in line:
                data.borderBottom = int(vaule)
            elif 'int paddingLeft =' in line:
                data.paddingLeft = int(vaule)
            elif 'int paddingRight =' in line:
                data.paddingRight = int(vaule)
            elif 'int paddingTop =' in line:
                data.paddingTop = int(vaule)
            elif 'int paddingBottom =' in line:
                data.paddingBottom = int(vaule)
            else:
                pass
    return picDatas


def cutPic(im, x, y, w, h, ofx, ofy, tw, th, savePath):
    if im:
        box = (x, y, x+w, y+h)
        region = im.crop(box)
        newImg = Image.new('RGBA', (tw, th))
        newImg.paste(region, (ofx, ofy))
        newImg.save(savePath)


loadFiles(".")
