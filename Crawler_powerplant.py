import requests
from bs4 import BeautifulSoup
from typing import Optional, List
import pandas as pd

class ScrapeMap:
    
    def __init__(self, url:str , headers:Optional[dict] = None):
        self.url = url
        #self.df = df
        self.headers = headers or {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    def parse(self, source = "") -> Optional[BeautifulSoup]:
        """
        source: "coal","wind","gas","biomass", etc...
        """
        if source:
            html = self.url + f"?source={source}"
        else:
            html = self.url
            
        session = requests.Session()
        try:
            resp = session.get(html , headers = self.headers)
            resp.raise_for_status()
        except Exception as e:
            print(f"Request failed:{e}")
            return None
        
        print("MISSION SUCCESS!")
        return BeautifulSoup(resp.text , "html.parser")
    
    
    def getName(self, bs) -> List[str]:
        names = bs.find_all('td', attrs = {'class':'row-name'})
        nameList = [name.text.strip() for name in names]
        return nameList
    
    def getEnName(self, bs) -> List[str]:
        enNames =  bs.find_all('td',  attrs = {'class':'row-subhead'})
        enNameList = [name.text.strip() for name in enNames]
        return enNameList
    
    def getOperator(self, bs) -> List[str]:
        operator = bs.find_all('td',  attrs = {'data-label':'Operator'})
        opList = [op.text.strip() for op in operator]
        return opList
    
    def getOutput(self, bs) -> List[str]:
        output = bs.find_all('td',  attrs = {'data-label':'Power'})
        outputList = [out.text.strip() for out in output]
        return outputList
    
    def export(self, bs) -> pd.DataFrame:

        if bs is None:
            print("No content to export.")
            return None
        
        df = pd.DataFrame({
            "Name": self.getName(bs),
            "English Name": self.getEnName(bs),
            "Operator": self.getOperator(bs),
            "Output": self.getOutput(bs)
        })
        return df
    
def crawler(source: str = "", url:str = "https://openinframap.org/stats/area/China/plants"):
    scraper = ScrapeMap(url = url)
    bs = scraper.parse(source)
    return scraper.export(bs)

if __name__ == '__main__':
    data = crawler()

