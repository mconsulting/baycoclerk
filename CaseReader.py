from asyncio.log import logger
from datetime import datetime
from importlib.resources import path
from operator import concat
from textwrap import indent
from typing import Dict
from bs4 import BeautifulSoup
import os
import pandas as pd
import logging
import json
from datetime import datetime
class case_reader(object):
   


    def read_all(self):
       res={}

       #summary
       #parties
       #events
       #dockets

       res["summary"]
       res["parties"]
       res["events"]
       res["dockets"]=self.dockets

       return res

    def __init__(self,path_to_file) -> None:
        #logging.basicConfig(filename='case_reader.log', level=logging.DEBUG,
        #            format='%(asctime)s|%(levelname)s|%(message)s')
        #logging.debug(path_to_file)
        self.props={}
        self.parties={}
        self.events={}
        self.dockets={}
        
        self.path=path_to_file
        self.name=str(path_to_file).split("\\")[-1]
        self.prefix = self.name.split("_")[0].upper()
        self.html=open(path_to_file).read()
        self.soup=BeautifulSoup(self.html,"html.parser")
        
        self.get_summary()

    def get_summary(self):
        tbl=self.soup.find(id="summaryAccordion")
        rows=tbl.find_all("dd")
       
        self.case_num=rows[1].text.strip()
        obj={}
        for row in rows:
            prop=row.attrs['class'][0].strip()
         
            val=row.text.strip()
            obj[prop]=val
            
            #obj=json.dumps({"case_num":self.case_num,"property":prop,"value":val},indent=3)
        #myDict=Dict.fromkeys(cols,vals)
        #obj["prefix"]=self.prefix.strip()

        #obj["status"]="Case loaded"
       # obj["prefix"]=self.prefix
        self.judge= obj["judge"] # rows[0].text.strip()
        self.case_num=obj["casenumber"]
        self.courttype=obj["courttype"]
        self.props=obj
        
        

        return self.props
        

    def get_parties(self):
        #logger.debug("TODO: get_parties()")
        grid=self.soup.find(id="gridParties")
        if grid is not None:
            rows=grid.find_all("tr")
       
            data=[]
            for i in range(1,len(rows)):
                row=rows[i]
                cols=row.find_all("td")
                
                party_type=cols[0].text.strip()
                party_name=cols[1].text.strip()
                rawstring=cols[2].text.replace("(Main Attorney)","").strip()
                if len(rawstring.splitlines())>0:
                    attorney_name=[x.strip() for x in rawstring.splitlines() if len(x.strip())>4][0]
                else:
                    attorney_name=""
                    
                new_row={"party_type": party_type,"party_name":party_name,"attorney_name": attorney_name,"casenumber": str(self.case_num)}
                
                data.append(new_row)
            df=pd.DataFrame(data=data,columns=["party_type","party_name","attorney_name","casenumber"])
            
            return df

    def get_charges(self):
        grid=self.soup.find(id="gridCharges")
        if grid is not None:
            headers=[h.text.strip() for h in grid.find("thead").find_all("th")]
            headers.append('casenumber')
            rows=grid.find("tbody").find_all("tr")
            data=[]

            for row in rows:
                new_row=[col.text.strip() for col in row.find_all("td")]
                new_row.append(self.case_num)
                #new_row={"Count": eventdate,"casenumber": str(self.case_num), "description":description}
                data.append(new_row)

            df=pd.DataFrame(data=data,columns=headers)
            
           
            return df
    def get_events(self):
        grid=self.soup.find(id="gridCaseEvents")
        if grid is not None:
            headers=[h.text.strip() for h in grid.find("thead").find_all("th")][:-1]
            headers.append('casenumber')
            rows=grid.find("tbody").find_all("tr")
            data=[]

            for row in rows:
                vals=[col.text.strip() for col in row.find_all("td")]
                vals.append(self.case_num)
                data.append(vals)
               
            if len(data[0])==2:
                data=None
            df=pd.DataFrame(data=data,columns=headers)
            df["casenumber"]=self.case_num
            return df

    def log_event(self,source,message):
        hist=self.props["history"]
        timenow=datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        log_entry={"source":source,"message":message,"event_date_time":timenow}
        hist.append(log_entry)
        #logging.debug(message)

    def get_dockets(self):
        
        grid=self.soup.find(id="gridDockets")
        if grid is not None:
            rows=grid.find_all("tr")
       
            bfound=False
            data=[]
            for i in range(2,len(rows)):
                row=rows[i]
                cols=row.find_all("td")
                
                eventdate=cols[1].text.strip()
                description=cols[2].text.strip()
                if self.prefix in str(description):  # we are going from newest to oldest so we can just overwrite the
                                                #old value if there are multiple instances of the search term in the list
                    #self.props["first_appeared"]=eventdate
                    bfound=True
                    #self.props["status"] += "Search term " + self.prefix + " found"
                   
                new_row={"eventdate": eventdate,"casenumber": str(self.case_num), "description":description}
                data.append(new_row)


            if bfound==False:
                print(self.prefix + " not in " + self.name)
                #self.props["first_appeared"]=self.props["clerkfiledate"]
                #self.props["status"] = "Search term " + self.prefix + " NOT found"
           # logging.debug(data)
            df=pd.DataFrame(columns=["eventdate","casenumber","description"],data=data)
            return df

        else:
            logging.debug("gridDockets not found")
        #df.to_csv("csv\\" + self.name.replace(".htm","_dockets.csv"))

      


errorlist=[]


Parties=[]
Dockets=[]
Summaries=[]
Charges=[]
Events=[]

htmlfiles=[x for x in os.listdir("htm") if x.endswith(".htm")]
for i,f in enumerate(htmlfiles):
    print(i,f)
   
    cr=case_reader("htm\\" + f)
    Events.append(cr.get_events())
    Charges.append(cr.get_charges())
    Dockets.append(cr.get_dockets())
    Summaries.append(cr.props)
    Parties.append(cr.get_parties())
    
 
    
dfDockets=pd.concat(Dockets)
dfDockets_clean=dfDockets[dfDockets["description"] != '']
dfDockets_clean["eventdate"]=pd.to_datetime(dfDockets_clean["eventdate"])
dfDockets_clean.to_csv("all_dockets.csv")

dfSummaries=pd.DataFrame(Summaries)
dfSummaries["statusdate"]=pd.to_datetime(dfSummaries["statusdate"])
dfSummaries["clerkfiledate"]=pd.to_datetime(dfSummaries["clerkfiledate"])
dfSummaries.to_csv("all_summaries.csv")

dfParties=pd.concat(Parties)
dfParties.to_csv("all_parties.csv")

dfCharges=pd.concat(Charges)
dfCharges.to_csv("all_charges.csv")

dfEvents=pd.concat(Events)
dfEvents.to_csv("all_events.csv")

print(dfCharges.head())
