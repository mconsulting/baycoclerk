# %%
import os
import re
import pandas as pd

# %%

os.getcwd()

os.listdir()
        

# %%
df=pd.read_csv("Tract_Instrument.csv")
df
mcclain=df[df["Instrument"].str.startswith("McClain-")==True]
blaine=df[df["Instrument"].str.startswith("Blaine-")==True]
grady=df[df["Instrument"].str.startswith("Grady-")==True]

# %%
for row in mcclain["Tract"]:
    pattern="\d{1,2}[N,S]\d{1,2}[E,W]"
    matches=re.findall(pattern,row)
    print(row)
    if len(matches)>0:
        sbuff=matches[0] 
        twpregex= "\d{1,2}[N,S]"
        idx=sbuff.find(matches[0])
        sections=row.
        twp="T" + re.search(twpregex,sbuff)[0]
        rngregex=""
        rng="R" + re.search("\d{1,2}[E,W]",sbuff)[0]
        print(twp,rng)

# %%
strbuff="31 8N4W"




