from telegram.ext import Updater
from telegram.ext import CommandHandler , MessageHandler, Filters , ConversationHandler , CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
import telegram

import keyboards

import json
import pymongo
import logging
import threading

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.DEBUG)
config = json.load(open("config.json"))
client = pymongo.MongoClient(config["db"]["host"], config["db"]["port"])
db = client[config["db"]["db_name"]]

COUNTRYDEP,CITYDEP,AIRPORTDEP = range(3)
COUNTRYARR, CITYARR,AIRPORTARR = range(3,6)
LOCATION_INFO = range(6,7)
YEAR_D,MONTH_D,DAY_D = range(7,10)
YEAR_A,MONTH_A,DAY_A = range(10,13)
ADULTS,CHILDREN,INFANTS = range(13,16)

def start(update, contex):
    user_id = update.effective_chat.id
    
    if db.users.find_one({'user_id':user_id})==None:
        first_name = update.message.chat.first_name
        last_name = update.message.chat.last_name
        username = update.message.chat.username
        reg_dict = {'user_id':user_id,'username':username,
                    'first_name':first_name,'last_name':last_name}
        db.users.insert_one(reg_dict)
    user_query= db.users.find_one({'user_id':user_id})
    update.message.reply_text(text=config['messages']['welcome'], reply_markup=keyboards.countries_menu)
    
    return COUNTRYDEP
def countryDep(update, contex):
    chat_id =  update.effective_chat.id
    query_data = update.callback_query.data
    contex.user_data["country_d"]=query_data
    text = config['messages']['city_d'].format(contex.user_data["country_d"])
    contex.bot.send_message(chat_id =chat_id, text=text , 
                            reply_markup=keyboards.generate_city(contex.user_data["country_d"]),
                            parse_mode=telegram.ParseMode.MARKDOWN)
    return CITYDEP
def cityDep(update,contex):
    chat_id = update.effective_chat.id
    query_data = update.callback_query.data
    contex.user_data['city_d']=query_data
    text = config['messages']['airport_d'].format(contex.user_data['country_d'],contex.user_data['city_d'])
    contex.bot.send_message(chat_id=chat_id,
                            text=text,reply_markup=keyboards.generate_airport(contex.user_data['city_d']), 
                            parse_mode=telegram.ParseMode.MARKDOWN)
    return AIRPORTDEP
def airportDep(update, contex):
    chat_id = update.effective_chat.id
    query_data = update.callback_query.data
    contex.user_data['airport_d']=query_data
    text = config['messages']['country_a'].format(contex.user_data['country_d'],
                                                  contex.user_data['city_d'],
                                                  contex.user_data['airport_d'])
    contex.bot.send_message(chat_id=chat_id , 
                            text=text, reply_markup=keyboards.countries_menu,
                            parse_mode=telegram.ParseMode.MARKDOWN)
    return COUNTRYARR
    
def countryArr(update,contex):
    chat_id = update.effective_chat.id
    query_data = update.callback_query.data
    contex.user_data['country_a']=query_data
    text = config['messages']['city_a'].format(contex.user_data['country_a'])
    contex.bot.send_message(chat_id=chat_id, 
                            text=text, 
                            reply_markup=keyboards.generate_city(contex.user_data['country_a']),
                            parse_mode=telegram.ParseMode.MARKDOWN)
    return CITYARR
def cityArr(update,contex):
    chat_id = update.effective_chat.id
    query_data = update.callback_query.data
    contex.user_data['city_a']=query_data
    text = config['messages']['airport_a'].format(contex.user_data['city_a'],contex.user_data['country_a'])
    contex.bot.send_message(chat_id=chat_id, 
                            text=text, 
                            reply_markup=keyboards.generate_airport(contex.user_data['city_a']),
                            parse_mode=telegram.ParseMode.MARKDOWN)
    
    return AIRPORTARR

def airportArr(update,contex):
    chat_id = update.effective_chat.id 
    query_data = update.callback_query.data
    contex.user_data['airport_a']=query_data
    text_i = config['messages']['travel_info']
    # asking year for departure
    text_m = config['messages']['year'].format('Departure')
    contex.bot.send_message(chat_id=chat_id,
                            text=text_i)
    contex.bot.send_message(chat_id=chat_id,
                            text=text_m,
                            reply_markup=keyboards.years_menu,
                            parse_mode=telegram.ParseMode.MARKDOWN)
    return YEAR_D
def ask_month_d(update,contex):
    chat_id = update.effective_chat.id
    year = update.message.text.strip()
    contex.user_data['year_d']=year
    #ask for month of departure
    text = config['messages']['month'].format('Departure')
    contex.bot.send_message(chat_id=chat_id,
                            text=text,
                            reply_markup=keyboards.generate_month(int(contex.user_data['year_d'])),
                            parse_mode=telegram.ParseMode.MARKDOWN)
    return MONTH_D
def ask_day_d(update,contex):
    chat_id = update.effective_chat.id
    #month of departure
    month_word = update.message.text.strip()
    months = [('January', 1), ('February', 2), ('March', 3), ('April', 4), 
              ('May', 5), ('June', 6), ('July', 7), ('August', 8), ('September', 9), 
              ('October', 10), ('November', 11), ('December', 12)]
    month= [x[1] for x in months if x[0].lower()==month_word.lower()][0]
    contex.user_data['month_d']=month
    text = config['messages']['day'].format('Departure')
    contex.bot.send_message(chat_id=chat_id,
                            text=text,
                            reply_markup=keyboards.generate_days(int(contex.user_data['year_d']),int(contex.user_data['month_d'])),
                            parse_mode=telegram.ParseMode.MARKDOWN)
    return DAY_D
def ask_year_a(update,contex):
    chat_id = update.effective_chat.id
    day = update.message.text.strip()
    contex.user_data['day_d']=day
    #Ask year of Arrival
    text = config['messages']['year'].format('Arrival')
    contex.bot.send_message(chat_id=chat_id,
                            text=text,
                            reply_markup=keyboards.years_menu,
                            parse_mode=telegram.ParseMode.MARKDOWN)
    return YEAR_A
def ask_month_a(update,contex):
    chat_id = update.effective_chat.id
    year = update.message.text.strip()
    contex.user_data['year_a']=year
    text = config['messages']['month'].format('Arrival')
    contex.bot.send_message(chat_id=chat_id,
                            text=text,
                            reply_markup=keyboards.generate_month(int(contex.user_data['year_a'])),
                            parse_mode=telegram.ParseMode.MARKDOWN)
    return MONTH_A
def ask_day_a(update,contex):
    chat_id = update.effective_chat.id
    #month of arrival
    month_word = update.message.text.strip()
    months = [('January', 1), ('February', 2), ('March', 3), ('April', 4), 
              ('May', 5), ('June', 6), ('July', 7), ('August', 8), ('September', 9), 
              ('October', 10), ('November', 11), ('December', 12)]
    month= [x[1] for x in months if x[0].lower()==month_word.lower()][0]
    contex.user_data['month_a']=month
    text = config['messages']['day'].format('Arrival')
    contex.bot.send_message(chat_id=chat_id,
                            text=text,
                            reply_markup=keyboards.generate_days(int(contex.user_data['year_a']),int(contex.user_data['month_a'])),
                            parse_mode=telegram.ParseMode.MARKDOWN)
    return DAY_A
def adult(update,contex):
    chat_id = update.effective_chat.id
    day = update.message.text.strip()
    contex.user_data['day_a']=day
    text = config['messages']['adults']
    contex.bot.send_message(chat_id=chat_id,
                            text=text,
                            reply_markup=keyboards.number_menu,
                            parse_mode=telegram.ParseMode.MARKDOWN)
    return ADULTS
def children(update,contex):
    chat_id = update.effective_chat.id
    adults = update.message.text.strip()
    contex.user_data['adults']=adults
    text = config['messages']['children']
    contex.bot.send_message(chat_id=chat_id,
                            text=text,
                            reply_markup=keyboards.number_menu,
                            parse_mode=telegram.ParseMode.MARKDOWN)
    return CHILDREN
def infants(update, contex):
    chat_id = update.effective_chat.id
    children = update.message.text.strip()
    contex.user_data['children']=children
    text = config['messages']['infants']
    contex.bot.send_message(chat_id=chat_id,
                            text=text,
                            reply_markup=keyboards.number_menu,
                            parse_mode=telegram.ParseMode.MARKDOWN)
    return INFANTS 
def search(update,contex):
    chat_id = update.effective_chat.id
    infant = update.message.text.strip()
    contex.user_data['infants']=infant
    text = config['messages']['all_info'].format(contex.user_data['country_d'],
                                                 contex.user_data['city_d'],
                                                 contex.user_data['airport_d'],
                                                 contex.user_data['year_d'],
                                                 contex.user_data['month_d'],
                                                 contex.user_data['day_d'],
                                                 contex.user_data['country_a'],
                                                 contex.user_data['city_a'],
                                                 contex.user_data['airport_a'],
                                                 contex.user_data['year_a'],
                                                 contex.user_data['month_a'],
                                                 contex.user_data['day_a'],
                                                 contex.user_data['adults'],
                                                 contex.user_data['children'],
                                                 contex.user_data['infants'])
    contex.bot.send_message(chat_id=chat_id,
                            text=text,
                            parse_mode=telegram.ParseMode.MARKDOWN)
def one_way(update,contex):
    chat_id = update.effective_chat.id 
    text = config['messages']['one_way']
    contex.bot.send_message(chat_id=chat_id,
                            text=text,
                            parse_mode=telegram.ParseMode.MARKDOWN)
    text_i = config['messages']['travel_info']
    # asking year for departure
    text_m = config['messages']['year'].format('Departure')
    contex.bot.send_message(chat_id=chat_id,
                            text=text_i)
    contex.bot.send_message(chat_id=chat_id,
                            text=text_m,
                            reply_markup=keyboards.years_menu,
                            parse_mode=telegram.ParseMode.MARKDOWN)
    return YEAR_D
    
def main():
    updater = Updater(token=config['TOKEN'], use_context=True)
    dispatcher = updater.dispatcher
    conv = ConversationHandler(
        entry_points = [CommandHandler('start', start)],
        states = {
            COUNTRYDEP: [CallbackQueryHandler(countryDep)],
            CITYDEP: [CallbackQueryHandler(cityDep)],
            AIRPORTDEP: [CallbackQueryHandler(airportDep)],
            COUNTRYARR: [CallbackQueryHandler(countryArr)],
            CITYARR: [CallbackQueryHandler(cityArr)],
            AIRPORTARR: [CallbackQueryHandler(airportArr)],
            YEAR_D: [MessageHandler(Filters.regex(r'\d{4}'),ask_month_d)],
            MONTH_D: [MessageHandler(Filters.regex(r'^(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)(?i)[a-zA-Z]*'), ask_day_d)],
            DAY_D: [MessageHandler(Filters.regex(r'\d{1,2}'),ask_year_a)],
            YEAR_A:[MessageHandler(Filters.regex(r'\d{4}'),ask_month_a)],
            MONTH_A:[MessageHandler(Filters.regex(r'^(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)(?i)[a-zA-Z]*'),ask_day_a)],
            DAY_A:[MessageHandler(Filters.regex(r'\d{1,2}'),adult)],
            ADULTS:[MessageHandler(Filters.regex(r'\d{1,2}'),children)],
            CHILDREN:[MessageHandler(Filters.regex(r'\d{1,2}'),infants)],
            INFANTS:[MessageHandler(Filters.regex(r'\d{1,2}'),search)]
            
        },
        fallbacks = [CommandHandler('start', start)]
    )
    one_way_conv = ConversationHandler(
        entry_points=[CommandHandler('oneway',one_way)],
        states = {
            YEAR_D:[MessageHandler(Filters.regex(r'\d{4}'),ask_month_d)],
            MONTH_D: [MessageHandler(Filters.regex(r'^(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)(?i)[a-zA-Z]*'), ask_day_d)],
            DAY_D: [MessageHandler(Filters.regex(r'\d{1,2}'),adult)],
            ADULTS:[MessageHandler(Filters.regex(r'\d{1,2}'),children)],
            CHILDREN:[MessageHandler(Filters.regex(r'\d{1,2}'),infants)],
            INFANTS:[MessageHandler(Filters.regex(r'\d{1,2}'),search)]
        },
        fallbacks = [CommandHandler('oneway',one_way)]
    )


    dispatcher.add_handler(conv)
    dispatcher.add_handler(one_way_conv)
    
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()