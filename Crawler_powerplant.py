import requests
from bs4 import BeautifulSoup
from typing import Optional, List, Tuple
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

class ScrapeMap:
    
    def __init__(self, url:str , headers:Optional[dict] = None):
        self.url = url
        #self.df = df
        self.headers = headers or {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        self.session = requests.Session()
    
    def parse(self, source = "") -> Optional[BeautifulSoup]:
        """
        source: "coal","wind","gas","biomass"
        """
        if source:
            html = self.url + f"?source={source}"
        else:
            html = self.url
            
        session = requests.Session()
        try:
            resp = session.get(html , headers = self.headers)
        except Exception as e:
            print(f"Error:{e}")
            return None
        if resp.status_code == 200:
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
    
    def getMapLinks(self , bs4) -> List[str]:
        names = bs.find_all('td',attrs={'class':'row-name'})
        mapLinks = [name.a.attrs['href'] for name in names]
        return mapLinks
    
    def export(self, bs) -> pd.DataFrame:
        id_list = self.getIdList(bs)
        type_list = [self.getTypes(wid) for wid in id_list]
        
        df = pd.DataFrame({
            "Name": self.getName(bs),
            "English Name": self.getEnName(bs),
            "Operator": self.getOperator(bs),
            "Output": self.getOutput(bs),
            "Id": id_list,
            "Type":type_list
        })

        return df

    def getIdList(self , bs):
        names = bs.find_all('td',attrs={'class':'row-name'})
        links = [name.a.attrs['href'] for name in names]
        wayidList = [link.split('/')[-1] for link in links]
        return wayidList

    def getTypes(self , wayid):
        """
        根据ID判断出地址类型
        """
        if wayid.startswith('-'):
            return 'relation'
        else:
            return 'way'

    def getCoordinates(self, typ: str, wayid: str) -> Optional[Tuple[float, float]]:
        query = f"""
        [out:json];
        {typ}({abs(int(wayid))});
        out center;
        """
        api_url = "http://overpass-api.de/api/interpreter"

        try:
            resp = self.session.post(api_url, data={'data': query}, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            return data['elements'][0]['center']['lat'], data['elements'][0]['center']['lon']
        except Exception as e:
            print(f"Coordinate error for {typ} {wayid}: {e}")
            return None
        
    def _get_all_coordinates_parallel(self, id_list: List[str], type_list: List[str]) -> List[Optional[Tuple[float, float]]]:
        coords = [None] * len(id_list)
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_index = {
                executor.submit(self.getCoordinates, typ, wayid): i
                for i, (typ, wayid) in enumerate(zip(type_list, id_list))
            }
            for future in as_completed(future_to_index):
                i = future_to_index[future]
                try:
                    coords[i] = future.result()
                except Exception as e:
                    print(f"Error getting coordinate at index {i}: {e}")
        return coords