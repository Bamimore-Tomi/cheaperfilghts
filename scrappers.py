import requests
from bs4 import BeautifulSoup as BS
import pyshorteners
def quatar():
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
    url = 'https://www.cheapflights.co.uk/flight-search/LOS-JFK/2020-11-18/2020-12-09/1adults/children-1S-1S-11-11-15-15?sort=price_a'
    req = requests.get(url, headers=headers)
    soup = BS(req.content, parser='lxml')
session = requests.Session()
headers = {'user-agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
init_connection = session.get('https://www.cheapflights.co.uk', headers=headers)
url = 'https://www.cheapflights.co.uk/flight-search/LOS-JFK/2020-11-19/2020-12-12/1adults/children-1S-1S-1S-11-15-15?sort=bestflight_a'
req = session.get(url, headers=headers)
soup = BS(req.content,'lxml')
all_=soup.find_all('div',{"page-idx":"1"})
base_url = 'https://www.cheapflights.co.uk'
shortener_object = pyshorteners.Shortener()
data = []
for i in all_:
    airline_go = all_[i].find('div',{'class':'section times'}).find('div',{'class':'bottom'}).text.strip()
    depart_time_go = all_[i].find('div',{'class':'section times'}).find('span',{'class':'depart-time base-time'}).text.strip().replace('\n','')
    arrival_time_go = all_[i].find('div',{'class':'section times'}).find('span',{'class':'arrival-time base-time'}).text.strip().replace('\n','')
    stops_go = all_[i].find('div',{'class':'section stops'}).find('span',{'class':'stops-text'}).text.strip()
    airline_come = all_[i].find('li',{'class':'flight'}).find('div',{'class':'section times'}).text.strip().replace('\n','')
    depart_time_come = all_[i].find('li',{'class':'flight'}).find('div',{'class':'section times'}).find('span',{'class':'depart-time base-time'}).text.strip().replace('\n','')
    arrival_time_come = all_[i].find('li',{'class':'flight'}).find('div',{'class':'section times'}).find('span',{'class':'arrival-time base-time'}).text.strip().replace('\n','')
    stops_come = all_[i].find('li',{'class':'flight'}).find('div',{'class':'section stops'}).find('span',{'class':'stops-text'}).text.strip().replace('\n','')
    link_long= all_[i].find('div',{'class':'multibook-dropdown'}).find('a',{'class':'booking-link'}).attrs['href']
    link = shortener_object.tinyurl.short(base_url+link_long)
    price = all_[i].find('span',{'class':'price-text'}).text.strip()
    price_currency = price[:1]
    price_value = int(price[1:].replace(',',''))
    data.append({'AG':airline_go , 'DTG': depart_time_go,'ATG':arrival_time_go,'SG':stops_go,
                 'AC':airline_come,'DTC':depart_time_come,'ATC':arrival_time_come,'SC':stops_come,
                 'LL':link_long,'L':link, 'P':price,'PC':price_currency,'PV':price_value})
print(data)
