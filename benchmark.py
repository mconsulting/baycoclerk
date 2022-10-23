from concurrent.futures import thread
from datetime import datetime
import logging
from random import randint
from sqlite3 import Time
from threading import Thread
from selenium import webdriver
from PIL import Image
import time
import webbrowser
from selenium.webdriver.common.by import By
import codecs
import os
import pandas as pd
from bs4 import BeautifulSoup



class Benchmark(object):
    

    def download_html(self):
        html=self.driver.page_source
        try:

            soup=BeautifulSoup(html,"html.parser")
            var=soup.find(id="summaryAccordion")
            rows=var.find_all("dd")
            obj={}
            for row in rows:
                key=row.attrs['class'][0]
                val=row.text.strip()
                obj[key]=val
        
            judge= obj["judge"] # rows[0].text.strip()
            case_num=obj["casenumber"]
            courttype=obj["courttype"]
            #self.judge= rows[0].text.strip()
        # self.case_num=rows[1].text.strip()
            #new_row={"casenumber": str(self.case_num), "judge": str(self.judge)}
            fn=self.name + "_" + case_num + ".htm"
            with open("htm\\" + fn,"w") as f:
                f.write(html)
        
        except:
            print("error")
        
    def get_events(self):
    
        html=self.driver.page_source
        soup=BeautifulSoup(html,"html.parser")
        var=soup.find(id="gridDockets")
        rows=var.find_all("tr")
        casenumber=self.case_num
        
        data=[]
        for i in range(2,len(rows)):
            row=rows[i]
            cols=row.find_all("td")
            
            eventdate=cols[1].text.strip()
            description=cols[2].text.strip()
            
            new_row={"date": eventdate,"casenumber": str(self.case_num), "description":description}
            data.append(new_row)  

        df=pd.DataFrame(columns=["date","casenumber","description"],data=data)
        df.to_csv(self.name + "-" + self.case_num + "_events.csv")

    def __init__(self,search_text) -> None:
      
        self.driver=webdriver.Chrome("chromedriver.exe")
        self.url="https://court.baycoclerk.com/BenchmarkWeb2/Home.aspx/Search"
        self.name=search_text.strip()
        self.load_first_page(self.name)
        self.caselist=[]
    
    def export_list(self):
        fn="SearchResults.csv"
        if os.path.exists(fn):
            os.rename(fn,self.name + "_export.csv")
    
    def load_list(self):
        fn=self.name + "_export.csv"
        if os.path.exists(fn):
            self.data_frame=pd.read_csv(fn)
            return len(self.data_frame)

    def load_first_page(self,searchfor):
        self.driver.get(self.url)  
        time.sleep(2)
        search_by_name_textbox=self.driver.find_element(By.XPATH,"/html/body/div[3]/table/tbody/tr/td[2]/div/table/tbody/tr/td/table/tbody/tr[3]/td[2]/div/div/div[1]/div/div[1]/input")
        search_by_name_textbox.send_keys(searchfor)

   

        
    def select_100_records(self):
            xp="/html/body/div[3]/table/tbody/tr/td[2]/div/table/tbody/tr/td/table/tbody/tr[2]/td[2]/div[1]/div[3]/div[1]/label/select/option[4]"
            elm=self.driver.find_element(By.XPATH,xp)
            elm.click()

    def move_next(self):
        xp="/html/body/div[3]/table/tbody/tr/td[2]/div/table/tbody/tr/td/table[2]/tbody/tr[1]/td[2]/div[1]/div/ul/li[3]/a"
        button_next=self.driver.find_element(By.XPATH,xp)
        button_next.click()
        time.sleep(4)

    def get_cases_from_caselist(self):
        self.export_list()
        self.load_list()
        df=self.data_frame
        self.select_100_records()
        row_count=0
        error_count=0

        for i in range(len(df)):
            try:
                row_count=row_count+1
                print(i,row_count)
                
                casenumber=df.iloc[i,2]
                fn=self.name + "_" + casenumber + ".htm"
                if os.path.exists("htm\\" + fn):
                    continue
                case_link=self.driver.find_element(By.LINK_TEXT,casenumber)
                case_link.click()
                time.sleep(4)

                self.download_html()
                self.driver.back()
                time.sleep(2)
                if row_count % 100==0:
                    elem=self.driver.find_element(By.LINK_TEXT,"Next")
                    elem.click()
                    time.sleep(2)
                    row_count=0

            
            except:
                logging.error(casenumber)
                error_count = error_count + 1

        return i - error_count  #total rows less the errors


    def get_case_by_index(self, ordinal_position):
        try:
            xp=str.format("/html/body/div[3]/table/tbody/tr/td[2]/div/table/tbody/tr/td/table/tbody/tr[2]/td[2]/div[1]/table/tbody/tr[{}]/td[5]/a",str(ordinal_position))
            case_link=self.driver.find_element(By.XPATH,xp)
            casenumber=case_link.text.strip()
            print(casenumber)
            case_link.click()
            time.sleep(4)

            self.download_html()
            self.driver.back()
            time.sleep(2)
        except:
            print("error in get_case()" + str(ordinal_position))
    #def init_name_search(self,name_string):

def main():
    search_string="PELL, ROBERT ALLAN"

    scraper=Benchmark(search_string)

  #  atty.select_100_records()
    new_records=scraper.get_cases_from_caselist()
    
  
    case_count=int(scraper.driver.find_element(By.XPATH,"/html/body/div[3]/table/tbody/tr/td[2]/div/table/tbody/tr/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div[1]/div[1]/div[3]").text.strip().split("\n")[1])

    print(str(casecount) + " total cases for " + search_string)
    print(str(new_records) + " net records added")
   
  #  for i in range(1,case_count+1):
   #     print(i)   
    #    atty.get_case_by_index(i)
       # atty.get_summary()
       # atty.get_events()
       # atty.move_next()
        #df=pd.DataFrame(atty.caselist)
        #df.to_csv("csv\\" + search_string + "_caselist.csv")
main()