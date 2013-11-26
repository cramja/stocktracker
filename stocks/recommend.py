import random, datetime
from urllib import *

from stocks.models import Stock


#queries yahoo for the given symbol
#symbol = stock symbol as string
#time_period = datetime.timedelta object
# returns a csv string of finance data
def get_stock_data(symbol, time_period = datetime.timedelta(weeks=2)):
    pastDate = datetime.datetime.now() - time_period
    currDate = datetime.datetime.now()

    url = 'http://ichart.yahoo.com/table.csv?s={0}&a={1}&b={2}&c={3}&d={4}&e={5}&f={6}&g=d&ignore=.csv'.format(
        symbol, str(pastDate.month - 1), str(pastDate.day), str(pastDate.year),
        str(currDate.month - 1), str(currDate.day), str(currDate.year))

    try:
        histData = urlopen(url) #file like object...read with file reader
        data = histData.read()
        return str(data)
    except URLError as e:
        return e

#Date   Open    High    Low Close   Volume  Adj Close
#takes a raw Yahoo api string and removes excess text
#returns rows of csv data
def clean_stock_data(csv_string):
    rows = str(csv_String).split('\\n')
    rows = rows[1:len(rows)-1] #kill the first and last row
    #now we just have financial data
    return rows

# given a list of cleaned csv data
# returns whether or not this is a good stock
def analyze_data(cleaned_data):
    rising = 0
    falling = 0

    for row in cleaned_data:
        members = row.split(',')
        popen = float(members[1])
        pclose = float(members[4])
        if pclose-popen > 0:
            rising+=1
        else:
            falling+=1

    return rising > falling

# returns a boolean whether or not the user should buy
def run_recommendation_analysis(stock):
    if len(Stock.objects.filter(code=stock)) == 1:
        data = get_stock_data(stock) #should do error checking here
        rows = clean_stock_data(data)
        would_recommend = analyze_data(rows)
        return would_recommend
    else:
        return "error"
