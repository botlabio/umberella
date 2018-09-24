import sys
import datetime

from pandas import read_csv

def umbrella(months=None, days=None, lookback=None, verbose=0):
    
    '''Fetches daily top 1 million domains by DNS activity
    from Cisco's Umbrella. 
    
    Returns a list of unique domains and subdomains combined from 
    the selected days/months.
    
    MORE INFO
    =========
    http://s3-us-west-1.amazonaws.com/umbrella-static/index.html
   
   
    EXAMPLE USE
    ===========
    
    domains = umberella([6, 7, 8], range(31))
    
    or for auto mode: 
    
    domains = umberella()
    
    
    PARAMS
    ======
    
    months :: integer or list of integers
    
    days :: integer or list of integers
    
    lookback :: number of days to look back (useful for when months and days are None)
    
    verbose :: 0 for silent operation
   
    '''
    
    if lookback is None:
        lookback = 2

    if months is None:
        months = int(datetime.date.today().strftime("%m"))
        days = int(datetime.date.today().strftime("%d")) - lookback
    
    # deal with single day / month inputs
    if isinstance(months, int):
        months = [months]
    if isinstance(days, int):
        days = [days]
    
    # create the set for final results
    final = set([])

    # iterate through months
    for month in months:
        month = str(month).zfill(2)
        
        # iterate through days in the month
        for date in days:
            if date < 10:
                date = str(date + 1).zfill(2)
            else:
                date = str(date)

            # parse the url for the file of the day
            url = 'http://s3-us-west-1.amazonaws.com/umbrella-static/top-1m-2018-' + month + '-' + date +'.csv.zip'

            if verbose == 1:
                print("%s of %s month" % (date, month))
            
            # download the file and merge with final output set
            try:
                df = read_csv(url, compression='zip', header=None)
                out = set(df[1])
                final = final.union(out)

            # it's not so important if one day is missed
            except:
                print('Something went wrong with %s %s' % (date, month))

    return list(final)

if __name__ == '__main__':
    
    try:
        months = sys.argv[1]
        days = sys.argv[2]
    except IndexError:
        months = None
        days = None

    umberella(months, days)
