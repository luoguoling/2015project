#!/usr/bin/evn python
#coding:utf-8
import ansible.runner
import ansible.inventory
import json,time,writelog,random,sendsocket,getconfig,re
def AnsibleApi(AnsibleModuleName,AnsibleInventory,AnsibleCommand):
    ReturnMsg = {}
    runner = ansible.runner.Runner(
        module_name = AnsibleModuleName,
        inventory = AnsibleInventory,
        module_args = AnsibleCommand,
        environment = {'LANG':'zh_CN.UTF-8','LC_CTYPE':'zh_CN.UTF-8'},
        )
    ReturnValue = runner.run()
    #No hosts found
    if ReturnValue is None:
        ReturnMsg['code'] = "-1"
        ReturnMsg['msg'] = "hosts not found"
    #Failed
    for (hostname,result) in ReturnValue['contacted'].items():
        if 'failed' in result:
            ReturnMsg['code'] = "-2"
            ReturnMsg['msg'] = "%s,%s" %(hostname,result['msg'])
    #success
    for (hostname,result) in ReturnValue['contacted'].items():
        if result['rc'] == 0:
            ReturnMsg['code'] = "0"
            ReturnMsg['msg'] = result['stdout']
        else:
            ReturnMsg['code'] = str(result['rc'])
            ReturnMsg['msg'] = result['stderr']
    #host down
    for (hostname,result) in ReturnValue['dark'].items():
        ReturnMsg['code'] = "-3"
        ReturnMsg['msg'] = result
    return json.dumps(ReturnMsg)

def GetLogName(logPath,otherStyleTime,logHour,logType):
    loghours = []
    logName = ""
    CheckHour = {"code":"0","codemessage":"OK"}
    if logType == "hour":
        if logHour.strip():
            #split logHour
            LogHourSplit = logHour.split(',')
            for i in range(len(LogHourSplit)):
                LogHourSecondSplit = LogHourSplit[i].split('-')
                if int(len(LogHourSecondSplit)) == 2:
                    for b in range(int(LogHourSecondSplit[0]),int(LogHourSecondSplit[1])+1):
                        if b > 23:
                            CheckHour['code'] = "-1"
                            CheckHour['codemessage'] = "The Hour input is not valid"
                        elif len(str(b)) == 1:
                            loghours.append("0"+str(b))
                        else:
                            loghours.append(str(b))
                else:
                    if int(LogHourSplit[i]) > 23:
                        CheckHour['code'] = "-1"
                        CheckHour['codemessage'] = "The Hour input is not valid"
                    elif len(LogHourSplit[i]) == 1:
                        loghours.append("0"+LogHourSplit[i])
                    else:
                        loghours.append(LogHourSplit[i])
            if int(CheckHour['code']) == 0:
                curHour = time.strftime('%Y%m%d%H',time.localtime(time.time()))
                for p in range(len(loghours)):
                    if p == len(loghours) - 1:
                        if otherStyleTime + loghours[p] == curHour:
                            logName = logName + logPath + ".log"
                        else:
                            logName = logName + logPath + "." + otherStyleTime + loghours[p] + ".1.log"
                    else:
                        if loghours[p] == curHour:
                            logName = logName + logPath + ".log" + " "
                        else:
                            logName = logName + logPath + "." + otherStyleTime + loghours[p] + ".1.log" + " "
        else:
            logName = logPath + "." + otherStyleTime + "*"
    else:
        curDay = time.strftime('%Y%m%d',time.localtime(time.time()))
        if otherStyleTime == curDay:
            logName = logPath + ".log"
        else:
            logName = logPath + "." + otherStyleTime + "*"
    CheckHour['codemessage'] = logName
    return CheckHour


def CheckPhpLog(LogMsg):
    try:
        platformAlias = LogMsg['platformAlias']
        serverId = LogMsg['serverId']
        serverIp = LogMsg['serverIp']
        logPath = LogMsg['logPath']
        logTime = LogMsg['logTime']
        timeArray = time.strptime(logTime,"%Y-%m-%d")
        otherStyleTime = time.strftime("%Y-%m-%d",timeArray)
        logCount = LogMsg['logCount']
        hosts = [serverIp]
        LogFile = "%s.txt" %(otherStyleTime)  
        AnsibleModuleName = "command"
        AnsibleInventory = ansible.inventory.Inventory(hosts)
        AnsibleCommand = "tail -n %s /data/www/weblog/%s/%s/%s" %(logCount,platformAlias,logPath,LogFile)
        writelog.write(AnsibleCommand)
    except Exception,e:
        writelog.write(str(e))
    
    AnsibleApiResult = AnsibleApi(AnsibleModuleName,AnsibleInventory,AnsibleCommand)
    return AnsibleApiResult

def DownPhpLog(LogMsg):
    try:
        platformAlias = LogMsg['platformAlias']
        serverId = LogMsg['serverId']
        serverIp = LogMsg['serverIp']
        logPath = LogMsg['logPath']
        logTime = LogMsg['logTime']
        webroot = LogMsg['webroot']
        md5key = getconfig.getkey("keys","key_conmmand")
        LogFile = "%s.txt" %(logTime)
        logdir = "%s/weblog/%s/%s" %(webroot,platformAlias,logPath)
        addr = (serverIp,1002)
        remote_cmd = {"cmd":"getlogs","md5key":md5key,"logtype":"phplog","webroot":webroot,"logdir":logdir,"logname":LogFile}
        DownPhpLogRevalue = sendsocket.send_socket(addr,json.dumps(remote_cmd))
        return DownPhpLogRevalue
    except Exception,e:
        writelog.write(str(e))
        
def SearchJavaLog(LogMsg):
    try:
        platformAlias = LogMsg['platformAlias']
        serverId = LogMsg['serverId']
        serverIp = LogMsg['serverIp']
        logPath = LogMsg['logPath']
        logTime = LogMsg['logTime']
        timeArray = time.strptime(logTime,"%Y-%m-%d")
        otherStyleTime = time.strftime("%Y%m%d",timeArray)
        logHour = LogMsg['hour']
        logKey = LogMsg['key']
        logType = LogMsg['logtype']
        javaDir = LogMsg['javaDir']
        gameName = LogMsg['gamename']
        LogNameDict = GetLogName(logPath,otherStyleTime,logHour,logType)
        if int(LogNameDict['code']) == 0:
            logName = LogNameDict['codemessage']
        else:
            return '{"code":"-1","codemessage":"The Hour input is not valid"}'
        SearchRe = '[a-z0-9A-Z]*\_[0-9]*\_%s' %(gameName)
        basedir = "/data/chroot_javalogs/javalogs/%s/logs/" %(re.search(SearchRe,javaDir).group())
        hosts = [serverIp]
        AnsibleModuleName = "shell"
        AnsibleInventory = ansible.inventory.Inventory(hosts)
        AnsibleCommand = "cd %s && grep \"%s\" %s" %(basedir,logKey,logName)
        writelog.write(AnsibleCommand)
        AnsibleApiResult = AnsibleApi(AnsibleModuleName,AnsibleInventory,AnsibleCommand)
        return AnsibleApiResult
    except Exception,e:
        writelog.write(str(e))


def CheckJavaLog(LogMsg):
    try:
        platformAlias = LogMsg['platformAlias']
        serverId = LogMsg['serverId']
        serverIp = LogMsg['serverIp']
        logPath = LogMsg['logPath']
        logTime = LogMsg['logTime']
        lotAccount = LogMsg['logAccount']
        logType = LogMsg['logtype']
        javaDir = LogMsg['javaDir']
        gameName = LogMsg['gamename']
        timeArray = time.strptime(logTime,"%Y-%m-%d %H:%M:%S")
        SearchRe = '[a-z0-9A-Z]*\_[0-9]*\_%s' %(gameName)
        basedir = "/data/chroot_javalogs/javalogs/%s/logs/" %(re.search(SearchRe,javaDir).group())
        if logType == "hour":
            otherStyleTime = time.strftime("%Y%m%d%H",timeArray)
            if time.strftime('%Y%m%d%H',time.localtime(time.time())) == otherStyleTime:
                logName = basedir + logPath + ".log"
            else:
                logName = basedir + logPath + "." + otherStyleTime + ".1.log"
        else:
            otherStyleTime = time.strftime("%Y%m%d",timeArray)
            if time.strftime('%Y%m%d',time.localtime(time.time())) == otherStyleTime:
                logName = basedir + logPath + ".log"
            else:
                logName = basedir + logPath + "." + otherStyleTime + ".1.log"
        hosts = [serverIp]
        AnsibleModuleName = "shell"
        AnsibleInventory = ansible.inventory.Inventory(hosts)
        AnsibleCommand = "tail -n %s %s" %(lotAccount,logName)
        writelog.write(AnsibleCommand)
        AnsibleApiResult = AnsibleApi(AnsibleModuleName,AnsibleInventory,AnsibleCommand)
        return AnsibleApiResult
    except Exception,e:
        writelog.write(str(e))
        
def ExecJavaCmd(LogMsg):
    try:
        platformAlias = LogMsg['platformAlias']
        serverId = LogMsg['serverId']
        serverIp = LogMsg['serverIp']
        execCmd = LogMsg['execcommand']
        javaPid = LogMsg['javapid']
        hosts = [serverIp]
        AnsibleModuleName = "shell"
        AnsibleInventory = ansible.inventory.Inventory(hosts)
        AnsibleCommand = execCmd
        writelog.write(AnsibleCommand)
        AnsibleApiResult = AnsibleApi(AnsibleModuleName,AnsibleInventory,AnsibleCommand)
        return AnsibleApiResult
    except Exception,e:
        writelog.write(str(e))


def DownJavaLog(LogMsg):
    try:
        platformAlias = LogMsg['platformAlias']
        serverId = LogMsg['serverId']
        serverIp = LogMsg['serverIp']
        logPath = LogMsg['logPath']
        logType = LogMsg['logtype']
        logTime = LogMsg['logTime']
        webroot = LogMsg['webroot']
        javaDir = LogMsg['javaDir']
        checkTimeZone = LogMsg['checkTimeZone']
        gameName = LogMsg['gamename']
        timeArray = time.strptime(logTime,"%Y-%m-%d")
        otherStyleTime = time.strftime("%Y%m%d",timeArray)
        md5key = getconfig.getkey("keys","key_conmmand")
        LogNameDict = GetLogName(logPath,otherStyleTime,checkTimeZone,logType)
        SearchRe = '[a-z0-9A-Z]*\_[0-9]*\_%s' %(gameName)
        logdir = "/data/chroot_javalogs/javalogs/%s/logs" %(re.search(SearchRe,javaDir).group())
        if int(LogNameDict['code']) == 0:
            logName = LogNameDict['codemessage']
        else:
            return '{"code":"-1","codemessage":"The Hour input is not valid"}'
        addr = (serverIp,1002)
        remote_cmd = {"cmd":"getlogs","md5key":md5key,"logtype":"javalog","webroot":webroot,"logdir":logdir,"logname":logName}
        DownJavaLogRevalue = sendsocket.send_socket(addr,json.dumps(remote_cmd))
        return DownJavaLogRevalue
        writelog.write(str(remote_cmd))
    except Exception,e:
        writelog.write(str(e))
        
    