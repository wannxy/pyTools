import os,sys
from PIL import Image

G_folder = []
G_scale = 1

def merged(folder):
    all_image = {}

    newWidth = 0
    newHeigh = 0

    for filename in os.listdir(folder):
        if filename.endswith("jpg") and not filename.startswith("Ant"):
            img_path = os.path.join(folder,filename)
            img_data = Image.open(img_path)
            width,height = img_data.size
            newWidth += width
            newHeigh = height if height > newHeigh else newHeigh
            item = {"img_path":img_path,"img_data":img_data,"width":width,"height":height}
            all_image.update({filename[:-4]:item})
    if len(all_image) > 0:
        newImage = Image.new("RGB",(newWidth,newHeigh));
        px = 0
        for key in all_image:
            x = all_image[key]["width"]
            data = all_image[key]["img_data"]
            newImage.paste(data,(px,0))
            px += x
        newImage.resize((int(newImage.size[0] * float(G_scale)),int(newImage.size[1] * float(G_scale))))\
                .save(os.path.join(folder,"Ant.jpg"))

def parse(path):
    pl = os.listdir(path)
    for p in pl:
        if os.path.isdir(os.path.join(path,p)):
            G_folder.append(os.path.join(path,p))
            parse(os.path.join(path,p))
args = sys.argv
G_scale = args[2]
parse(".")
for p in G_folder:
    print("正在处理: [ %s ]" %p)
    merged(p)
    print("处理结束: [ OK ]")

