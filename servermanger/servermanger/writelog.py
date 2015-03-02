__author__ = 'Administrator'
import time,os
def write_log(local_logs):
    if not os.path.exists("disklogs"):
	try:
            os.mkdir("disklogs")
	except:
	    print 'can not mkdir'
    cur_time = time.strftime("%Y%m%d")
    logs = "["+time.strftime("%Y-%m-%d-%H-%M-%S")+"]: "+local_logs+"\n"
    file = open("logs/"+cur_time+".txt","a")
    file.write(logs)
    file.close()
