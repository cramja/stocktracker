import random, datetime
from urllib.request import urlopen
from urllib.error import URLError

from stocks.models import Stock

class stockData:
    def __init__(self, date, popen, pclose, phigh, plow, volume):
        self.date = str(date)
        self.open = float(popen)
        self.close = float(pclose)
        self.high = float(phigh)
        self.low = float(plow)
        self.volume = float(volume)

    def __unicode__(self):
        return self.date + " Open: " + str(popen)
    def __str__(self):
        return self.date + " Open: " + str(popen)
    #did the stock price rise on that interval?
    def is_rising(self):
        return self.open < self.close

    #true if self is greater than given stock
    def compare_open(self, comp):
        return self.open > comp.open



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

#0Date   1Open    2High    3Low 4Close   5Volume  6Adj Close
#takes a raw Yahoo api string and removes excess text
#returns rows stockData objects
def clean_stock_data(csv_string):
    rows = str(csv_string).split('\\n')
    rows = rows[1:len(rows)-1] #kill the first and last row
    #now we just have financial data
    stocks = []
    for datarow in rows:
        row = datarow.split(',')
        stock = stockData(row[0], row[1], row[4], row[2], row[3], row[5])
        stocks.append(stock)
    return stocks

# given a list of cleaned csv data
# returns whether or not this is a good stock to buy 
def analyze_data(cleaned_data):
    rising = 0
    falling = 0
    for stock in cleaned_data:
        if stock.is_rising():
            rising += 1
        else:
            falling += 1
    return (rising/2) >= falling

# returns a boolean whether or not the user should buy
def run_recommendation_analysis(stock):
    if len(Stock.objects.filter(code=stock)) == 1:
        data = get_stock_data(stock) #should do error checking here
        rows = clean_stock_data(data)
        would_recommend = analyze_data(rows)
        #assert False
        return would_recommend
    else:
        return "error"