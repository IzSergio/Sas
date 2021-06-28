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


def crops(img, ramka):
    arr = np.array(img)
    shape = np.array(arr.shape)
    shape[:2] += ramka*2
    newarr = np.zeros(shape, np.uint8)
    newarr[:ramka,:,:] = 0
    newarr[:,:ramka,:] = 0
    newarr[-ramka:,:,:] = 0
    newarr[:,-ramka:,:] = 0

    newarr[ramka:-ramka,ramka:-ramka,:] = arr
    return Image.fromarray(newarr)    


def makegraphs(img, cval):
    file = img.filename
    res = [file, #0
    '.'.join(file.split('.')[:-1])+'graph.png', #1
    '.'.join(file.split('.')[:-1])+'new.'+file.split('.')[-1], #2
    '.'.join(file.split('.')[:-1])+'newgraph.png', #3
    ]


    distr(img, name=res[0], f=res[1])

    img = crops(img,int(cval))
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
    }
    
    return res
