import requests
from bs4 import BeautifulSoup
import multiprocessing as mp
import sqlite3
import re

def scrape_weeklyPrices(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    data_list = list()
    
    for tr in soup.select("tbody tr"):
        try: 
            year = re.search(r"(\d+)", tr.find(class_="B6").text).group(1)
            for date, value in zip(tr.find_all(class_ = "B5"), tr.find_all(class_ = "B3")):
                if value.text.strip() != '':                    
                    try:
                        value = float(value.text.strip())
                    except ValueError:
                        value = None
                    data_list.append((f"{date.text.rstrip()}/{year}", value))
                    
        except AttributeError: # Occurs when 'tr' is an empty row
            pass
    return data_list
            
def scrape_monthlyPrices(url):
    months_dict = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    data_list = list()
    
    for tr in soup.find_all("tr"):
        try:
            year = tr.find(class_ = "B4").text.strip()
            month = 1
            for td in tr.find_all(class_ = "B3"):
                try:
                    value = float(td.text.strip())
                except ValueError:
                    value = None
                data_list.append((f"{months_dict[month]}/{year}",value))
                month += 1
        except AttributeError: # Occurs when 'tr' is an empty row
            pass
    return data_list
    
def scrape_annualPrices(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    data_list = list()
    
    for tr in soup.select("tbody tr"):
        decade = tr.find(class_="B4").text.strip()
        year = 0
        for value in tr.find_all(class_="B3"):
            try:
                value = float(value.text)
            except ValueError:
                if value == "":
                    break
                value = None
            data_list.append((f"Year-{year} {decade}", value))
            year += 1
            
    return data_list

class FuelPriceScraper:
    def __init__(self, fileName):
        self.home_url = "https://www.eia.gov/dnav/pet/pet_pri_gnd_a_epm{fuel_type}_pte_dpgal_{time_filter}.htm"
        self.base_url = "https://www.eia.gov/dnav/pet/"
        self.fuel_types = ("regular", "midgrade", "premium")
        self.time_filters = ("weekly", "monthly", "annually")
        
        self.conn = sqlite3.connect(fileName)
        self.cur = self.conn.cursor()
        
        self.table_fields = self.__getTableFields()
        self.pool = mp.Pool(len(self.table_fields))
        
        self.__createDB()
        self.__fillDB()
        
        self.conn.commit()
        self.conn.close()
        
    def __getTableFields(self):
        page = requests.get(self.home_url.format(fuel_type=self.fuel_types[0][0],time_filter=self.time_filters[0][0]))
        soup = BeautifulSoup(page.content, "lxml")
        return ['-'.join(tags.text.split()) for tags in soup.find_all(class_ = "DataStub1")]
    
    def __createDB(self):
        for fuel in self.fuel_types:
            for time in self.time_filters:
                tn = fuel+':'+time
                self.cur.execute(f"DROP TABLE IF EXISTS '{tn}'")
                self.cur.execute(f"CREATE TABLE '{tn}'(Time TEXT PRIMARY KEY)")
                for field in self.table_fields:
                    self.cur.execute(f"ALTER TABLE '{tn}' ADD COLUMN '{field}' REAL")
    
    def __fillDB(self):
        for f in self.fuel_types:
            for t in self.time_filters:
                time_filter_scraping_funcs = {'w':scrape_weeklyPrices, 'm':scrape_monthlyPrices, 'a':scrape_annualPrices}
                links = self.__scrapeLinks(self.home_url.format(fuel_type = f[0], time_filter = t[0]))
                price_list = self.pool.map(time_filter_scraping_funcs[t[0]], links)
                
                for data in price_list[0]:
                    period = self.__formatDate(t, data[0])
                    self.cur.execute(f"INSERT INTO '{f+':'+t}' (Time, '{self.table_fields[0]}') VALUES (?, ?)", (period, data[1]))  
                    
                for i in range(1, len(price_list)):
                    for data in price_list[i]:
                        period = self.__formatDate(t, data[0])
                        self.cur.execute(f"UPDATE '{f+':'+t}' SET ('{self.table_fields[i]}') = ? WHERE Time = ?", (data[1], period))

    def __formatDate(self, period, data):
        if period == "weekly":
            temp = data.split('/')
            return f'{temp[2]}-{temp[0]}-{temp[1]}'
        elif period == 'annually':
            match = re.match(r".+(\d+) (\d{3}).+", data).groups()
            return match[1]+match[0]
        return data
            
    def __scrapeLinks(self, url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "lxml")
        return [self.base_url+link.find("a")["href"][2:] for link in soup.find_all("td", class_="DataHist")]

    
if __name__ == "__main__":
    mp.set_start_method('spawn')  # to use spawn instead of fork on Mac/Linux
    FuelPriceScraper("fuelPrice.db")
