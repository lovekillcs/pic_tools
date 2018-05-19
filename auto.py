import sys
reload(sys)
sys.setdefaultencoding('gbk')
from collections import OrderedDict
import json
import shutil
import os
import commands


keys = ['act_0', 'act_1', 'act_2', 'act_3', 'act_4',
        'move_0', 'move_1', 'move_2', 'move_3', 'move_4',
        'stand_0', 'stand_1', 'stand_2', 'stand_3', 'stand_4', ]

dirs = ['up', 'upright', 'right', 'downright', 'down']

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
        if '.plist.meta' in f:
            analyzeMeta(f)


def analyzeMeta(path):
    # path = 'sequence.plist.meta'
    dataDict = {}
    with open(path, 'rb') as file:
        data = file.read()
        jsonData = json.loads(data)
        subMetas = jsonData['subMetas']
        for pic in subMetas:
            uuid = subTexture(subMetas[pic])

            for key in keys:
                if key in pic:
                    if not dataDict.has_key(key):
                        dataDict.setdefault(key, [{pic: uuid}])
                    else:
                        dataDict.get(key).append({pic: uuid})

        for v in dataDict.values():
            v.sort()

        for k, v in dataDict.items():
            createAni(path, k, v)


def createAni(path, key, data):

    frameCount = len(data)
    duration = frameCount / 12.0
    frameTime = duration / frameCount
    if '0' in key:
        dir = dirs[0]
    elif '1' in key:
        dir = dirs[1]
    elif '2' in key:
        dir = dirs[2]
    elif '3' in key:
        dir = dirs[3]
    else:
        dir = dirs[4]

    wrapMode = 2  

    if 'act' in key:
        wrapMode = 1

    path = path.replace('sequence.plist.meta', dir + '.anim')

    f = open(path, 'w')

    __fileComments = OrderedDict()

    __fileComments["__type__"] = "cc.AnimationClip"
    __fileComments["_name"] = dir
    __fileComments["_objFlags"] = 0
    __fileComments["_rawFiles"] = None
    __fileComments["_duration"] = duration
    __fileComments["sample"] = 12
    __fileComments["speed"] = 1
    __fileComments["wrapMode"] = wrapMode
    __fileComments["curveData"] = {
        "comps": {
            "cc.Sprite": {
                "spriteFrame": [
                ]
            }
        }
    }
    __fileComments["events"] = []

    # __fileComments = {
    #     "__type__": "cc.AnimationClip",
    #     "_name": "up",
    #     "_objFlags": 0,
    #     "_rawFiles": '',
    #     "_duration": duration,
    #     "sample": 12,
    #     "speed": 1,
    #     "wrapMode": 2,
    #     "curveData": {
    #         "comps": {
    #             "cc.Sprite": {
    #                 "spriteFrame": [
    #                 ]
    #             }
    #         }
    #     },
    #     "events": []
    # }

    spriteFrame = __fileComments.get('curveData').get(
        'comps').get('cc.Sprite').get('spriteFrame')

    for i, v in enumerate(data):
        frame = {
            "frame": i * frameTime,
            "value": {
                "__uuid__": v.values()[0]
            }
        }
        spriteFrame.append(frame)

    f.write(json.dumps(__fileComments))
    f.close()

    print dir+'.anim'


def subTexture(data):
    uuid = data['uuid']
    return uuid


loadFiles('.')
