


# for creating db index db.airports.create_index([("name",pymongo.ASCENDING),("city",pymongo.ASCENDING),("iata_code",pymongo.ASCENDING)])
import calendar
from datetime import datetime
def get_month(year):
    global months
    months = [('January', 1), ('February', 2), 
              ('March', 3), ('April', 4), ('May', 5), 
              ('June', 6), ('July', 7), ('August', 8), 
              ('September', 9), ('October', 10), ('November', 11), ('December', 12)]
    today = datetime.today()
    if year>today.year:
        return months
    if year<today.year:
        return 0
    month = today.month
    temp = [months[i:] for i in range(len(months)) if months[i][1]==month]
    return [x for sublist in temp for x in sublist]
def get_days(year,month):
    num_days = calendar.monthrange(year,month)[1]
    today = datetime.today()
    days=range(0)
    if today.month==month:
        days = [x for x in range(today.day, num_days+1)]
    else:
        days = [x for x in range(1, num_days+1)]
    return days
print(get_days(2021,12))
