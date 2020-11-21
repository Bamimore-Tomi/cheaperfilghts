import requests
from bs4 import BeautifulSoup as BS
import pyshorteners
## Function takes keyword arguements in this form from data parsed from the bot
## airport_d is the iata_code for the airpot of departure, e.g LOS for Muritala international airport Lagos
## airport_a is the iata_code for the airpot, e.g LOS for Muritala international airport
## date_d , this is the date for depature comes in the format of yyyy-mm-dd e.g 2020-11-21
## date_a , this is the date for the return trip. If the trip is not a round trip, None is passed as the value
## adults is the number of adults going on the trip (12yrs and above)
## children is the number of children going on the trip (3yrs-11yrs)
## infants is the number of infants going on the trip (0-2yrs)
def cheaperflights(airport_d=None,airport_a=None,date_d=None,date_a=None,adults=None,children=None,infants=None):
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
    ##Returns a where AG=Departure Airline, DTG=depature time going, ATG=Arrival time going SG=Number of stops going, AC=Airline Coming
    ##DTC=departure time coming ATC=Arrival time coming,SC=Number of stops coming,LL=Booking link, L=Shortened booking link
    ##PC is the currency of the price , PV=integer value of the currency
print(cheaperflights())
