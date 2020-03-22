import os,sys

def _help():
    print("rn.py option")
    print("option:")
    print("  --help 查看帮助")
    print("  --restore 恢复.rar")
    print("  --del 删除.rar")

def _del(isH):
    flist = os.listdir()
    for p in flist:
        if isH:
            if p.endswith(".rar"):
                newName = p[:-4] + ".z.z"
                os.rename(p,newName)
                print(p+"--->"+newName)
        else:
            if p.endswith(".z.z"):
                newName = p[:-4] + ".rar"
                os.rename(p,newName)
                print(p+"--->"+newName)
                
def _parser(strP):
    ptrs = {"--restore":(_del,False),"--del":(_del,True)}
    if strP in ptrs:
        ptrs[strP][0](ptrs[strP][1])
    else:
        if "--help" != strP:
            print("Invalid parameter!")
        _help()
            
args = sys.argv
if len(args) != 2:
    print("Invalid parameter!")
    _help()
    exit
else:
    _parser(args[1])
    



