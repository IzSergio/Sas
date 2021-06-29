if __name__=="__main__":
 print("Hello World!")
 
from PIL import Image, ImageEnhance
import matplotlib.pyplot as plt
import numpy as np

def distr(img, name, f):
    fig, ax = plt.subplots(figsize=(10, 10))
    res = np.array(img.histogram()).reshape(3,256)
    zer = np.arange(256)
    ax.fill_between(zer, res[0], alpha=0.4, color='red')
    ax.fill_between(zer, res[1], alpha=0.4, color='green')
    ax.fill_between(zer, res[2], alpha=0.4, color='blue')
    ax.set_xlabel('Color Intensity')
    ax.set_ylabel('Frequency')
    ax.set_title(name)
    fig.savefig(f)
    plt.cla()
    return res


def colorgen(colors):
    color = {'к':(255,0,0),
            'о':(255,127,39),
            'ж':(255,242,0),
            'з':(0,255,0),
            'г':(66,170,255),
            'с':(0,0,255),
            'ф':(139,0,255),
            'ч':(0,0,0),
            'б':(255,255,255),
             }
    i = 0
    while i < len(colors):
        yield color[colors[i]]
        i += 1
        if i == len(colors):
            i = 0

def create_border(img, width, arg):
    res = Image.new(img.mode,(img.size[0]+width*2, img.size[1]+width*2))
    sqwidth = res.width//10
    sqheight = res.height//10

    i = 0
    j = 0
    col = colorgen(arg)
    while i<10:
        j = 0
        while j<10:
            res.paste(next(col),(i*sqwidth,j*sqheight,(i+1)*sqwidth,(j+1)*sqheight))
            j += 1
        if (j*sqheight)!=img.height:
            res.paste(next(col),(i*sqwidth,j*sqheight,(i+1)*sqwidth,res.height))
        i += 1
    if (10*sqwidth!=res.width):
        for i in range(10):
            res.paste(next(col), (10 * sqwidth, i * sqheight, res.width, (i + 1) * sqheight-1))
    if (10*sqwidth!=res.height) and (10*sqwidth!=res.width):
        res.paste(next(col), (10 * sqwidth, 10 * sqheight, res.width, res.height))
    res.paste(img, (width, width))
    return res   


def makegraphs(img, cval, arg):
    file = img.filename
    res = [file, #0
    '.'.join(file.split('.')[:-1])+'graph.png', #1
    '.'.join(file.split('.')[:-1])+'new.'+file.split('.')[-1], #2
    '.'.join(file.split('.')[:-1])+'newgraph.png', #3
    '.'.join(file.split('.')[:-1])+'new2.png', #4
    ]


    distr(img, name=res[0], f=res[1])

    img = create_border(img,int(cval), arg)
    img.save(res[2])
    img.close()
    img = Image.open(res[2])

    distr(img, res[2], res[3])
    img.close()
    
    
    print('savepaths: {}'.format(res))
    res = {res[0]:'Исходная картинка', 
    res[1]:'График исходной картинки', 
    res[2]:'Картинка с рамкой {}'.format(float(cval)), 
    res[3]:'График с рамкой', 
    #res[4]:'"Шахматная" рамка с чередованием цветов', 
    }
    
    return res
