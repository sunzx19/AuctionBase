
"""
FILE: skeleton_parser.py
------------------

Skeleton parser for CS145 programming project . Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""

import sys
from json import loads
from re import sub

columnSeparator = "|"

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

"""
Returns true if a file ends in .json
"""
def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""

def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)

def escapeQuo(s):
    p=s.split('\"')
    new='\"\"'.join(p)
    new='\"'+new+'\"'
    return new


"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""
def parseJson(json_file):
    with open(json_file, 'r') as f:
        items = loads(f.read())['Items'] # creates a Python dictionary of Items for the supplied json file
        wc=open("category.dat",'a') 
        wu=open("user.dat",'a')
        wb=open("bid.dat",'a') 
        wi=open("item.dat",'a') 

        for item in items:
            ItemID = item['ItemID']
            Name_b=item['Name']
            Name=escapeQuo(Name_b)
            Category=item['Category']
            # with open("category.dat",'a') as wc:
            for category_b in Category:
                category=escapeQuo(category_b)
                wc.write(ItemID+'|'+category+'\n')
                # wc.close()
            Currently=transformDollar(item['Currently'])
            if 'Buy_Price' in item:
                Buy_Price=transformDollar(item['Buy_Price'])
            else:
                Buy_Price='\"Null\"'
            First_Bid=transformDollar(item['First_Bid'])
            Number_of_Bids=item['Number_of_Bids']
            Location_sell_b=item['Location']
            Location_sell=escapeQuo(Location_sell_b)
            Country_sell_b=item['Country']
            Country_sell=escapeQuo(Country_sell_b)
            User_sell=item['Seller']
            UserID_sell_b=User_sell['UserID']
            UserID_sell=escapeQuo(UserID_sell_b)
            Rating_sell=User_sell['Rating']
            Started_b=transformDttm(item['Started'])
            Started=escapeQuo(Started_b)
            Ends_b=transformDttm(item['Ends'])
            Ends=escapeQuo(Ends_b)
            Description_b=item['Description']
            if Description_b is None:
                Description='\"Null\"'
            else:
                Description=escapeQuo(Description_b)

            Bids=item['Bids']
            if Bids is not None:
                for bid in Bids:
                    Bid=bid['Bid']
                    Amount=transformDollar(Bid['Amount'])
                    Time_b=transformDttm(Bid['Time'])
                    Time=escapeQuo(Time_b)
                    Bidder=Bid['Bidder']
                    UserID_bid_b=Bidder['UserID']
                    UserID_bid=escapeQuo(UserID_bid_b)
                    Rating_bid=Bidder['Rating']
                    if 'Location' in Bidder:
                        Location_bid_b=Bidder['Location']
                        Location_bid=escapeQuo(Location_bid_b)
                    else:
                        Location_bid='\"Null\"'

                    if 'Country' in Bidder:
                        Country_bid_b=Bidder['Country']
                        Country_bid=escapeQuo(Country_bid_b)
                    else:
                        Country_bid='\"Null\"'

                    wu.write(UserID_bid+'|'+Rating_bid+'|'+Location_bid+'|'+Country_bid+'\n')
                    wb.write(ItemID+'|'+UserID_bid+'|'+Time+'|'+Amount+'\n')            

            wi.write(ItemID+'|'+Name+'|'+Currently+'|'+Buy_Price+'|'+First_Bid+'|'+Number_of_Bids+'|'+Started+'|'+Ends+'|'+UserID_sell+'|'+Description+'\n')
            wu.write(UserID_sell+'|'+Rating_sell+'|'+Location_sell+'|'+Country_sell+'\n')

        wc.close()
        wu.close()
        wb.close()
        wi.close()

                

                



        """
        TODO: traverse the items dictionary to extract information from the
        given `json_file' and generate the necessary .dat files to generate
        the SQL tables based on your relation design
        """


"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_json_parser.py <path to json files>'
        sys.exit(1)
    # loops over all .json files in the argument
    for f in argv[1:]:
        if isJson(f):
            parseJson(f)
            print "Success parsing " + f


if __name__ == '__main__':
    main(sys.argv)
