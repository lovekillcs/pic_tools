import urllib2
import os
import math
import shutil
from PIL import Image
import re 

re_digits = re.compile(r'(\d+)')  

def emb_numbers(s):  
    pieces=re_digits.split(s)  
    pieces[1::2]=map(int,pieces[1::2])      
    return pieces  
  
def sort_strings_with_emb_numbers(alist):  
    aux = [(emb_numbers(s),s) for s in alist]  
    aux.sort()  
    return [s for __,s in aux]  
  
def sort_strings_with_emb_numbers2(alist):  
    return sorted(alist, key=emb_numbers)  


def down_image(url, file_name):
    _headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
    req = urllib2.Request(url=url, headers=_headers)
    binary_data = urllib2.urlopen(req).read()
    temp_file = open(file_name, 'wb')
    temp_file.write(binary_data)
    temp_file.close()


def load():
    for i in range(1, 1024):
        index = str(i)
        down_image("https://cdn2.cqllh5.jiulingwan.com/client2/res/map6/map_newcomer/map_newcomer_" +
                   index+".jpg", "map/map_newcomer_"+index+".jpg")


def mergePic(path):
    savePath = path+"result.jpg"
    if os.path.exists(savePath):    
        os.remove(savePath)

    files = os.listdir(path)
    count = len(files)
    tmp = Image.open(path + files[0])
    wc = math.sqrt(count)
    totalwidth = int(wc * tmp.width)
    newImg = Image.new('RGB', (totalwidth, totalwidth))
    w = h = tmp.width
    index = 0

    files = sort_strings_with_emb_numbers2(files)

    for f in files:
        im = Image.open(path + f)
        newImg.paste(im, ( int(w * (index % wc)), h * int(index / wc)))
        index += 1

    newImg.save(path+"result.jpg")


    # newImg = Image.new('RGBA', (256, 256))
    # newImg.paste(region, (128+ofx, 128+ofy))
    # newImg.save(savePath)
mergePic("map/")

# load()
