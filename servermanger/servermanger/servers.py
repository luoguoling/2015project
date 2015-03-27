import MySQLdb
import MySQLdb.cursors
class serverinfo:
    def serverinfo(self):
        myDb = MySQLdb.connect(host="127.0.0.1",port=5849,user='select', passwd='abc123?', db='serverlist', cursorclass=MySQLdb.cursors.DictCursor)
        myCurs = myDb.cursor()
        myCurs.execute("SELECT id,agent,ip,zone,gamedatadbname,javadir FROM gameserverinfo where isdelete!=1 order by zone")
        firstRow = myCurs.fetchall()
        return firstRow
    def agentsinfo(self):
        myDb = MySQLdb.connect(host="127.0.0.1",port=5849,user='select', passwd='abc123?', db='serverlist', cursorclass=MySQLdb.cursors.DictCursor)
        myCurs = myDb.cursor()
        myCurs.execute("SELECT distinct(agent) FROM gameserverinfo where isdelete!=1")
        firstRow = myCurs.fetchall()
        return firstRow 

