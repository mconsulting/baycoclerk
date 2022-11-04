import os
import shutil

htmlfiles=[x for x in os.listdir("htm") if x.endswith(".htm") and "_" in x]

os.chdir("htm")
for x in htmlfiles:
    if os.path.exists(x.split("_")[1])==False:
        os.rename(x,x.split("_")[1])
    else:
        os.remove(x)