import datetime,time
__author__ = 'Administrator'
def getCurrentTime():
    curtime = time.strftime('%Y%m%d%H%M',time.localtime(time.time()))
    return curtime
