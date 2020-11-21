from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
import utils
import json
import pymongo
import logging
import threading

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.DEBUG)
config = json.load(open("config.json"))
client = pymongo.MongoClient(config["db"]["host"], config["db"]["port"])
db = client[config["db"]["db_name"]]


countries = ['Belgium', 'Cameroon', 'Canada', 'China', 'Egypt', 'Germany', 'Ghana', 
             'India', 'Israel', 'Italy', 'Jamaica', 'Malaysia', 'New Zealand', 
             'Nigeria', 'Russia', 'Saudi Arabia', 'South Africa', 'Spain', 
             'United Arab Emirates', 'United Kingdom', 'United States']

countries_menu = InlineKeyboardMarkup([[InlineKeyboardButton('Belgium', callback_data='Belgium') ,  InlineKeyboardButton('Cameroon', callback_data='Cameroon')] , 
  [InlineKeyboardButton('Canada', callback_data='Canada') ,  InlineKeyboardButton('China', callback_data='China')] , 
  [InlineKeyboardButton('Egypt', callback_data='Egypt') ,  InlineKeyboardButton('Germany', callback_data='Germany')] , 
  [InlineKeyboardButton('Ghana', callback_data='Ghana') ,  InlineKeyboardButton('India', callback_data='India')] , 
  [InlineKeyboardButton('Israel', callback_data='Israel') ,  InlineKeyboardButton('Italy', callback_data='Italy')] , 
  [InlineKeyboardButton('Jamaica', callback_data='Jamaica') ,  InlineKeyboardButton('Kenya', callback_data='Kenya')],
  [InlineKeyboardButton('Malaysia', callback_data='Malaysia') , InlineKeyboardButton('New Zealand', callback_data='New Zealand')] ,  
  [InlineKeyboardButton('Nigeria', callback_data='Nigeria'),InlineKeyboardButton('Russia', callback_data='Russia') ],
  [InlineKeyboardButton('Saudi Arabia', callback_data='Saudi Arabia'), InlineKeyboardButton('South Africa', callback_data='South Africa')],
  [InlineKeyboardButton('Spain', callback_data='Spain'), InlineKeyboardButton('United Arab Emirates', callback_data='United Arab Emirates')],
  [InlineKeyboardButton('United Kingdom', callback_data='United Kingdom') ,  InlineKeyboardButton('United States', callback_data='United States')]])
def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu
def generate_city(country='Nigeria'):
    q = db.airports.find({'country':country})
    cities = []
    for i in q:
        cities.append(i['city'])
    cities = sorted(cities)
    cities_buttons = [InlineKeyboardButton(x,callback_data=x) for x in cities]
    cities_menu = InlineKeyboardMarkup(build_menu(cities_buttons,3))
    return cities_menu
def generate_airport(city='Lagos'):
    q = db.airports.find({'city':city})
    airports = []
    for i in q:
        airports.append(i['name']+','+i['iata_code'])
    airports = sorted(airports)
    airports_buttons = [InlineKeyboardButton(x,callback_data=x.split(',')[-1].strip()) for x in airports]
    airports_menu = InlineKeyboardMarkup(build_menu(airports_buttons,1))
    return airports_menu
years_menu = ReplyKeyboardMarkup([[KeyboardButton(text=2020), KeyboardButton(text=2021)],
                             [KeyboardButton(text=2022), KeyboardButton(text=2023)] ],
                            resize_keyboard=True,one_time_keyboard=True)
number_menu = ReplyKeyboardMarkup(build_menu([KeyboardButton(text=x) for x in range(0,9)],3),
                                  resize_keyboard=True,one_time_keyboard=True)
def generate_month(year):
    months = utils.get_month(year)
    months_buttons = [KeyboardButton(text=x[0]) for x in months]
    months_menu = range(0)
    if len(months_buttons) <3:
        months_menu = ReplyKeyboardMarkup(build_menu(months_buttons,1),
                                          resize_keyboard=True,one_time_keyboard=True)
    else:
        months_menu = ReplyKeyboardMarkup(build_menu(months_buttons,2),
                                          resize_keyboard=True,one_time_keyboard=True)
    return months_menu
def generate_days(year,month):
    days = utils.get_days(year,month)
    days_buttons = [KeyboardButton(text=x) for x in days]
    days_menu = ReplyKeyboardMarkup(build_menu(days_buttons , len(days_buttons)//6),
                                    resize_keyboard=True,one_time_keyboard=True)
    return days_menu
    
    
if __name__ == '__main__':
    generate_city()