from PIL import Image
import os

PATH = "";
OUT_PATH = PATH + "mirror/"

def main():
    for img in files():
        opt(img)

def opt(imgName):
    with Image.open(PATH + imgName) as orginImg:
        newImg = orginImg.transpose(Image.FLIP_LEFT_RIGHT)
        out(newImg,imgName)
        
def out(img,name):
    if not os.path.exists(OUT_PATH):
        os.mkdir(OUT_PATH)
    img.save(OUT_PATH + name, subsampling=0)
    print("[已完成] " + OUT_PATH + name)

def files():
    for root,dirs,files in os.walk(PATH):
        return files
    
if __name__ == "__main__":
    PATH = os.getcwd() + "/"
    main()
