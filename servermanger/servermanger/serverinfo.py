import MySQLdb
import MySQLdb.cursors
def serverinfo():
    myDb = MySQLdb.connect(host="127.0.0.1",port=5849,user='select', passwd='abc123?', db='serverlist', cursorclass=MySQLdb.cursors.DictCursor)
    myCurs = myDb.cursor() 
    myCurs.execute("SELECT id,agent,zone FROM gameserverinfo where isdelete!=1")
    firstRow = myCurs.fetchall()
    return firstRow
