#!/usr/bin/python
from PIL import Image

# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

import sys
reload(sys)
sys.setdefaultencoding('gbk')
import json
import shutil
import os
import commands


def cutFiles(path):
    pathList = []
    files = os.listdir(path)
    for f in files:
        if os.path.splitext(f)[1] == '.json':
            resName, typeName, subtextures = resolveJson(f)
            if os.path.isfile(resName + ".png"):
                t = resName.split('_')
                savePath = "result/" + t[0]+t[1]+"_" + typeName
                if "act" in resName:
                    savePath += "/attack/"
                elif "move" in resName:
                    savePath += "/run/"
                elif "stand" in resName:
                    savePath += "/stand/"

                # if os.path.exists(savePath):
                #     shutil.rmtree(savePath)

                if not os.path.exists(savePath):
                    os.makedirs(savePath)

                img = Image.open(resName + ".png")
                for pic in subtextures:
                    data = subtextureJson(subtextures[pic])
                    cutPic(img, data[0], data[1],
                           data[2], data[3], data[4], data[5], savePath + pic + ".png")

                if savePath not in pathList:
                    pathList.append(savePath)

    for path in pathList:
        picPacker(path)


# def picPacker():
#     files = os.listdir(path)
#     for f in files:

def resolveJson(path):
    with open(path, "rb") as file:
        data = file.read()
        fileJson = json.loads(data)
        resName = fileJson["resName"]
        typeName = fileJson["typeName"]
        subtexture = fileJson["subtexture"]
        return resName, typeName, subtexture


def subtextureJson(data):
    x = data['x']
    y = data['y']
    width = data['width']
    height = data['height']
    ofx = data['ofx']
    ofy = data['ofy']
    return int(x), int(y), int(width), int(height), int(ofx), int(ofy)


def cutPic(im, x, y, w, h, ofx, ofy, savePath):
    if im:
        box = (x, y, x+w, y+h)
        region = im.crop(box)
        newImg = Image.new('RGBA', (256, 256))
        newImg.paste(region, (128+ofx, 128+ofy))
        newImg.save(savePath)


def picPacker(sPath):
    dPath = sPath.replace("result", "packer_result")
    if os.path.exists(dPath):
        shutil.rmtree(dPath)

    # if os.path.exists("animation_template"):
    #     shutil.copytree("animation_template",dPath)
    # else:
    os.makedirs(dPath)
    # _sPath = os.path.abspath(sPath)
    # _dPath = os.path.abspath(dPath)
    cmd = "TexturePacker.exe --sheet "+dPath+"sequence.png --data "+dPath + \
        "sequence.plist --allow-free-size --trim --max-size 1024 --format cocos2d "+sPath
    os.system(cmd)


# print sys.getdefaultencoding()

cutFiles('.')
