import pandas as pd
import os

class attorney:

    def __init__(self) -> None:
        self.dockets=pd.read_csv("all_dockets.csv")
        
    def Search(self,search_list):
        
