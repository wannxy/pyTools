###切记切记 扫描顺序是左上->右下
import os
from PIL import Image

G_BOX =              (8,160,36,184)                    #x,y,x1,y2
G_BOX_SIZE =         (G_BOX[2]-G_BOX[0],G_BOX[3]-G_BOX[1])  #(宽，高)
G_BOX_PIXEL_AMOUNT = (G_BOX_SIZE[0]+1)*(G_BOX_SIZE[1]+1)    #区域的像素数量,+1是因为包含区域边界
G_BOX_Z =            0                                      #Z轴的高度或者说是有几张图片

def img2pixel(img):
    ###转储图片的像素，并构造以下结构
    img_data = {
        "width"    :0 , #图片的宽度
        "height"   :0 , #图片的高度
        "filename" :"", #图片的文件名
        "pixel"    :[], #图片的像素列表，包含了位置及三原色 #[0,0,(255,255,255)]
        "box"      :[]  #需要计算的区域字典，包含了位置及三原色 #[0,0,(255,255,255)]
        }
    img_data["filename"] = img
    data = Image.open(img)
    img_data["width"] = data.size[0]
    img_data["height"] = data.size[1]
    pixelTmp = []
    for h in range(0,img_data["height"]):
        for w in range(0,img_data["width"]):
            pixel = data.getpixel((w,h))
            #这里存放了图片的所有像素，如果使用请放开，如果不实用注释以提高性能
            #img_data["pixel"].append([w,h,pixel])
            if w >= G_BOX[0] and w <= G_BOX[2] and h >= G_BOX[1] and h <= G_BOX[3]:
                img_data["box"].append([w,h,pixel])
    return img_data
    
def loadFiles(path):
    ###加载目录下符合要求的文件并返回它们
    useFiles = []
    fl = os.listdir(path)
    print(">>>   正准备加载图片")
    for f in fl:
        if not os.path.isdir(f) and (f.endswith("png") or f.endswith("bmp")) and not f.startswith("mh"):
            useFiles.append(f)
    global G_BOX_Z
    G_BOX_Z = len(useFiles)
    return useFiles

def compare(data):
    result = []
    R,G,B = 0,0,0 #存放的是色差，而非颜色!!!
    for i in range(0,G_BOX_PIXEL_AMOUNT):
        R_MAX,R_MIN,G_MAX,G_MIN,B_MAX,B_MIN = 0,255,0,255,0,255
        for z in range(0,G_BOX_Z):
            R_MAX = R_MAX if R_MAX > data[z]["box"][i][2][0] else data[z]["box"][i][2][0]
            R_MIN = R_MIN if R_MIN < data[z]["box"][i][2][0] else data[z]["box"][i][2][0]
            G_MAX = G_MAX if G_MAX > data[z]["box"][i][2][1] else data[z]["box"][i][2][1]
            G_MIN = G_MIN if G_MIN < data[z]["box"][i][2][1] else data[z]["box"][i][2][1]
            B_MAX = B_MAX if B_MAX > data[z]["box"][i][2][2] else data[z]["box"][i][2][2]
            B_MIN = B_MIN if B_MIN < data[z]["box"][i][2][2] else data[z]["box"][i][2][2]
            R = (R_MAX - R_MIN) /255;
            G = (G_MAX - G_MIN) /255;
            B = (B_MAX - B_MIN) /255;
        result.append((data[z]["box"][i][0],
                       data[z]["box"][i][1],
                       "{: f}".format(round(R,6)),
                       "{: f}".format(round(G,6)),
                       "{: f}".format(round(B,6)),
                       round((R+G+B)/3,5),
                       "{: x}{: x}{: x}".format(data[z]["box"][i][2][0],data[z]["box"][i][2][1],data[z]["box"][i][2][2])))
    return result

            
def process():
    files = loadFiles(".")
    TEMP = []
    for img_file in files:
        print(">>>   正在处理：" + img_file)
        TEMP.append(img2pixel(img_file))
    rgb = compare(TEMP)
    rgb.sort(key = lambda k:k[5],reverse = False)
    for i in range(0,len(rgb)):
        print(rgb[i])


process()
