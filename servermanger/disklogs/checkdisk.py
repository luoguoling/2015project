#coding:utf-8
import threading
from datetime import datetime
import time
import os
import smtplib
#from email.mime.text import MIMEText
from email.MIMEText import MIMEText
#from email.Header import Header
#from log import logger
import logging,os,time,atexit,sys
from signal import SIGTERM
import subprocess
import socket,fcntl,struct
def write_log(local_logs):
    if not os.path.exists("disklogs"):
	try:
            os.mkdir("disklogs")
	except:
	    print 'can not mkdir'
    cur_time = time.strftime("%Y%m%d")
    logs = "["+time.strftime("%Y-%m-%d-%H-%M-%S")+"]: "+local_logs+"\n"
    file = open("disklogs/"+cur_time+".txt","a")
    file.write(logs)
    file.close()
def disk_stat():
    hd = {}
    disk = os.statvfs("/data")
    free = (disk.f_bavail * disk.f_frsize)
    total =(disk.f_blocks * disk.f_frsize)
    used  = (disk.f_blocks - disk.f_bfree) * disk.f_frsize*1.024
    try:
        percent = (float(used) / total) * 100
    except error:
#        get_log().info('calucate error')
	pass
    return percent
def get_log():
    logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    filename='myapp.log',
    filemode='w')
    logger = logging.getLogger('root')
    return logger
def backup_time():
    now = time.mktime(datetime.now().timetuple())-60*2
    result = time.strftime('%Y%m%d', time.localtime(now))
    backupresult = str(result)
    return backupresult
def send_email(content):
 
    sender = "lgl15984@163.com"
    receiver = ["992975991@qq.com","luoguoling@mokylin.com"]
    host = 'smtp.163.com'
    port = 465
    msg = MIMEText(content)
    msg['From'] = "lgl15984@163.com"
    msg['To'] = "992975991@qq.com"
    msg['Subject'] = "harddisk check"
 
    try:
    	smtp = smtplib.SMTP()
    	smtp.connect('smtp.163.com:25')
#   smtp.ehlo()
#   smtp.starttls()
#   smtp.ehlo()
    
#        smtp = smtplib.SMTP_SSL(host, port)
        smtp.login(sender, '15984794312')
        smtp.sendmail(sender, receiver, msg.as_string())
#        getlog().info("send email success")
    except Exception, e:
#        get_log().error(e)
        pass
    file.close()
def get_ip(ifname):
    s  = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(),0x8915,struct.pack('256s',ifname[:15]))[20:24])

def check():
    percent = disk_stat()
    write_log(str(percent))
#    get_log().info(percent)
    ip = get_ip('eth0')
    if int(percent) > 70:
        result = ip  + "   disusage: " + str(percent)
        write_log(result)
        os.popen('find /data/back -mtime +0 -exec rm -rf {} \; > /dev/null 2>&1')
	    
    elif int(percent) > 85:
	   result = ip  + "   disusage: " + str(percent) + "dangerous"
           write_log(result)
	   os.popen('rm -f /data/back/*')
    else:
        result = "false"
    return result
def task():
    while  True:
        result = check()
	if result == "false":
	    pass
	else:
            try:
                send_email(result)
            except:
	        pass
#        break
	time.sleep(1*60)
def run_monitor():
    monitor = threading.Thread(target=task)
    monitor.start()
# def createDaemon():
#     #脱离父进程
#     try:
#         pid = os.fork()
#         if pid > 0:
#             os._exit(0)
#     except OSError,error:
#         print "fork #1 failed: %d (%s)" % (error.errno, error.strerror)
#         os._exit(1)
#     #修改当前的工作目录
#     os.chdir('/')
#     #脱离终端
#     os.setsid()
#     #重设文件创建权限
#     os.umask(0)
#     #第二次创建进程，禁止进程重新打开终端文件
#     try:
#         pid = os.fork()
#         if pid > 0:
#             print 'Daemon PID %d' % pid
#             os._exit(0)
#     except OSError,error:
#         print "fork #1 failed: %d (%s)" % (error.errno, error.strerror)
#         os._exit(1)
#     run_monitor()
class Daemon:
    def __init__(self,pidfile,homedir,stderr='/dev/null',stdout='/dev/null',stdin='/dev/null'):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile
        self.homedir = homedir
    def _daemonize(self):
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError,e:
            sys.stderr.write("fork #1 failed: %d (%s) \n" % (e.errno,e.strerror))
            sys.exit(1)
        os.setsid()
        os.chdir('/')
        os.umask(0)
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError,e:
            sys.stderr.write("fork #1 failed: %d (%s) \n" % (e.errno,e.strerror))
            sys.exit(1)
        sys.stdout.flush()
        sys.stderr.flush()
        si = file(self.stdin,'r')
        so = file(self.stdout,'a+')
        se = file(self.stderr,'a+',0)
        os.dup2(si.fileno(),sys.stdin.fileno())
        os.dup2(so.fileno(),sys.stdout.fileno())
        os.dup2(se.fileno(),sys.stderr.fileno())
        atexit.register(self.delpid)
        pid = str(os.getpid())
        file(self.pidfile,'w+').write("%s\n" % pid)
    def delpid(self):
        os.remove(self.pidfile)
    def start(self):
        try:
            pf = file(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
        if pid:
            message = "pidfile %s already exist. Daemon already running?\n"
            sys.stderr.write(message)
            sys.exit(1)
        self._daemonize()
        self._run()
    def stop(self):
        try:
            pf = file(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
        if not pid:
            message = "pidfile % does not exist,Daemon not running?\n"
            sys.stderr.write(message)
            return
        try:
            while 1:
                os.kill(pid,SIGTERM)
                time.sleep(0.1)
        except OSError,err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
                else:
                    print str(err)
                    sys.exit(1)
    def restart(self):
        self.stop()
        self.start()
    def _run(self):
        pass
class Mydaemon(Daemon):
    def _run(self):
        run_monitor()
def main():
    homedir = os.getcwd()
    for i in ('log','run'):
        path = homedir + '/' + i
        if not os.path.exists(path):
            os.makedirs(path,0755)
    stdout = homedir + '/log' + '/server.log'
    stderr = homedir + '/log' + '/server.err'
    pidfile = homedir + '/run' + '/server.pid'
    daemon = Mydaemon(pidfile,homedir,stdout=stdout,stderr=stderr)
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            print 'start daemon'
            daemon.start()
        elif 'stop' == sys.argv[1]:
            print 'stop daemon'
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            print 'restart daemon'
            daemon.restart()
        else:
            print 'Unknown command'
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
if __name__ == "__main__":
    main()
# if __name__ == "__main__":
#     run_monitor()




