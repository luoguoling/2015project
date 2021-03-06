__author__ = 'Administrator'
# -*- coding: utf-8 -*-
import MySQLdb
from servermanger import settings
class db_operate:
    def mysql_command(self,conn,sql_cmd):
        try:
            ret = []
            conn=MySQLdb.connect(host=conn["host"],user=conn["user"],passwd=conn["password"],db=conn["database"],port=conn["port"],charset="utf8")
            cursor = conn.cursor()
            n = cursor.execute(sql_cmd)
            for row in cursor.fetchall():
                for i in row:
                    ret.append(i)
        except MySQLdb.Error,e:
            ret.append(e)
        return ret
    def mysqlinfo_command(self,conn,sql_cmd):
        try:
            ret = []
            conn=MySQLdb.connect(host=conn["host"],user=conn["user"],passwd=conn["password"],db=conn["database"],port=conn["port"],charset="utf8")
            cursor = conn.cursor()
            n = cursor.execute(sql_cmd)
            serverinfo = cursor.fetchall()
        except MySQLdb.Error,e:
            print 'mysql error'
        return  serverinfo

    def select_table(self,conn,sql_cmd,parmas):
        try:
            ret = []
            conn=MySQLdb.connect(host=conn["host"],user=conn["user"],passwd=conn["password"],db=conn["database"],port=conn["port"],charset="utf8")
            cursor = conn.cursor()
            n = cursor.execute(sql_cmd,parmas)
            for row in cursor.fetchall():
                for i in row:
                    ret.append(i)
        except MySQLdb.Error,e:
            ret.append(e)

        return ret
    def serverInfo(self):

        sql = 'select id,agent,zone from gameserverinfo where isdelete!=1'
        db = db_operate()
        serverInfo1 = db.mysqlinfo_command(settings.LOGMANGER_MYSQL,sql)
        return serverInfo1
    def checkAgent(self):
         sql = 'select distinct(agent) from gameserverinfo where isdelete!=1'
         db = db_operate()
         checkAgentlist = db.mysqlinfo_command(settings.LOGMANGER_MYSQL,sql)
         return checkAgentlist



