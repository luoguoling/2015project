__author__ = 'Administrator'
from mysql import db_operate
from servermanger import settings
class select_ip:
    def selectip(self,platformAlias,serverId):
        sql = 'select ip from gameserverinfo where agent="%s" and zone="%s"' %(platformAlias,serverId)
        db = db_operate()
        serverIp1 = db.mysql_command(settings.LOGMANGER_MYSQL,sql)
        for serverIp in serverIp1:
            return serverIp


