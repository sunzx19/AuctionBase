import web

db = web.database(dbn='sqlite',
        db='AuctionBase.db' #TODO: add your SQLite database filename
    )

######################BEGIN HELPER METHODS######################

# Enforce foreign key constraints
# WARNING: DO NOT REMOVE THIS!
def enforceForeignKey():
    db.query('PRAGMA foreign_keys = ON')

# initiates a transaction on the database
def transaction():
    return db.transaction()
# Sample usage (in auctionbase.py):
#
# t = sqlitedb.transaction()
# try:
#     sqlitedb.query('[judge QUERY STATEMENT]')
#     sqlitedb.query('[SECOND QUERY STATEMENT]')
# except Exception as e:
#     t.rollback()
#     print str(e)
# else:
#     t.commit()
#
# check out http://webpy.org/cookbook/transactions for examples

# returns the current time from your database
def getTime():
    # TODO: update the query string to match
    # the correct column and table name in your database
    query_string = 'select Curr_Time from CurrentTime'
    results = query(query_string)
    # alternatively: return results[0]['currenttime']
    return results[0].Curr_Time # TODO: update this as well to match the
                                  # column name

# returns a single item specified by the Item's ID in the database
# Note: if the `result' list is empty (i.e. there are no items for a
# a given ID), this will throw an Exception!
def getItemById(item_id):
    # TODO: rewrite this method to catch the Exception in case `result' is empty
    query_string = 'select * from Item where ItemID = $itemID'
    try:
        result = query(query_string, {'itemID': item_id})
        return result[0]
    except len(result)==0 as e:
        print e

def getUserById(user_id):
    query_string = 'select * from User where UserID = $userID'
    try:
        result = query(query_string, {'userID': user_id})
        return result[0]
    except len(result)==0 as e:
        print e

def getCategoryById(item_id):
    query_string = 'select * from Category where ItemID = $ItemID'
    result = query(query_string, {'ItemID': item_id})
    return result

def getBidById(item_id):
    query_string = 'select * from Bid where ItemID = $ItemID order by Time desc'
    result = query(query_string, {'ItemID': item_id})
    return result

def getStatusById(item_id):
    query_string = 'select * from Item where ItemID = $ItemID and (Currently < Buy_Price or Buy_Price is NULL)and Started <= (select Curr_time from CurrentTime) and Ends > (select Curr_time from CurrentTime)'
    result = query(query_string, {'ItemID': item_id})
    if len(result) != 0:
        return 'open'
    query2= 'select * from Item where ItemID = $ItemID and (Currently >= Buy_Price or Ends <= (select Curr_time from CurrentTime) )'
    result2 = query(query2, {'ItemID': item_id})
    if len(result2) != 0:
        return 'close'
    else:
        return 'not started'

# wrapper method around web.py's db.query method
# check out http://webpy.org/cookbook/query for more info
def query(query_string, vars = {}):
    return list(db.query(query_string, vars))

#####################END HELPER METHODS#####################

#TODO: additional methods to interact with your database,
# e.g. to update the current time
def updateTime(time):
    query_string='update CurrentTime set Curr_Time= $time'
    
    t = transaction()
    try:
        db.query(query_string,{'time':time})
    except:
        t.rollback()
        return 'Time set failed'
    else:
        t.commit()
        return 'Time set succeed!'


def addBid(item_id,user_id,time,amount):
    query_string='insert into Bid values ($item_id,$user_id,$time,$amount)'

    t = transaction()
    try:
        db.query(query_string,{'item_id':item_id,'user_id':user_id,'time':time,'amount':amount})
    except:
        t.rollback()
        return False
    else:
        t.commit()
        return True

def search(itemID, category,  minprice, maxprice, description, status):
    query_string = 'select * from Item where '
    var = {}
    judge = True
    if (itemID != ''):
        query_string += ' ItemID in (select ItemID from Item where ItemID = $ItemID)'
        var['ItemID'] = itemID
        judge = False 
    
    query_category=' ItemID in (select ItemID from Item where ItemID in (select ItemID from Category where Category = $Category))'
    if (category != '' and  judge == True):    
        query_string += query_category
        var['Category'] = category
        judge = False
    elif (category != '' and judge == False):
        query_string += ' and '+ query_category
        var['Category'] = category

    query_minprice=' ItemID in (select ItemID from Item where Currently >= $min_price)'
    if (minprice != '' and judge == True):
        query_string += query_minprice
        var['min_price'] = minprice
        judge = False
    elif (minprice != '' and judge == False):
        query_string += ' and '+ query_minprice 
        var['min_price'] = minprice

    query_maxprice=' ItemID in (select ItemID from Item where Currently <= $max_price)'
    if (maxprice != '' and judge == True):
        query_string += query_maxprice
        var['max_price'] = maxprice
        judge = False
    elif (maxprice != '' and judge == False):
        query_string += ' and '+query_maxprice 
        var['max_price'] = maxprice

    query_description=' ItemID in (select ItemID from Item where Description like $description)'
    if (description != '' and judge == True):    
        query_string += query_description
        var['description'] = '%' + description + '%'
        judge = False
    elif (description != '' and judge == False):
        query_string += ' and '+query_description
        var['description'] = '%' + description + '%'

    query_open=  '(Currently < Buy_Price or Buy_Price is NULL) and Started <= (select Curr_time from CurrentTime) and Ends > (select Curr_Time from CurrentTime)'
    query_close= '(Currently >= Buy_Price or Ends < (select Curr_Time from CurrentTime))'
    query_notstarted= 'Started >= (select Curr_Time from CurrentTime)'
    if (status == 'open' and judge == True):
        query_string += query_open
        judge = False;
    elif(status == 'open' and judge == False):
        query_string += ' and '+query_open
    elif (status == 'close' and judge == True):
        query_string += query_close
        judge=False
    elif (status == 'close' and judge == False):
        query_string += ' and '+query_close
    elif (status == 'notStarted' and judge== True):
        query_string += query_notstarted
        judge=False
    elif (status == 'notStarted' and judge== False):
        query_string += ' and '+query_notstarted

    if judge==True:
        query_string='select * from Item'
    result = query(query_string, var)
    return result
