import os
import shutil
import pandas as pd

def HTML_Cleanup():
    htmlfiles=[x for x in os.listdir("htm") if x.endswith(".htm") and "_" in x]

    os.chdir("htm")
    for x in htmlfiles:
        if os.path.exists(x.split("_")[1])==False:
            os.rename(x,x.split("_")[1])
        else:
            os.remove(x)


def CSV_Cleanup():
    csvs=[x for x in os.listdir("csv") if x.endswith("export.csv")]
    dfs=[]
    os.chdir("csv")
    for x in csvs:
        print(x)
        df=pd.read_csv(x,index_col=['Name','Case Number'])
        print(df)
        dfs.append(df)
        
        
    df_all=pd.concat(dfs)

    df_all.to_csv('search_results.csv')


def find_first_event(attorney,casenumber):
    
    

CSV_Cleanup()