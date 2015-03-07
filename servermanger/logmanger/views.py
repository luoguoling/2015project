#coding:utf-8
from django.shortcuts import render
# Create your views here.
from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.db import connection,models
from logmanger.models import AddLogpath
from logmanger.models import AddPhpLogpath
from logmanger.models import addCommand
import MySQLdb
import json,urllib
import logging,time
import ansible.runner,ansible.inventory
from django.http import HttpResponse
from servermanger.mysql import  db_operate
from servermanger.selectip import select_ip
from servermanger.selectPlatformAlias import select_platformAlias
from servermanger.writelog import write_log
from servermanger.splithour import splithour
from servermanger.AnsibleApi import AnsibleApi
from servermanger.SocketSend import socket_send
from servermanger.selectip import select_ip
from servermanger.getCurrentTime import getCurrentTime
from servermanger import settings
from django.contrib.auth import authenticate,login
from logmanger.forms import LoginForm
from django.contrib.auth.decorators import login_required,permission_required
"""main"""
#@login_required(login_url='login')
def index(request):
    return render_to_response('index.html')
def Nopri(request):
    return render_to_response('403.html')
"""login"""
def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render_to_response('login.html',RequestContext(request,{'form':form}))
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username,password=password)
            response = HttpResponseRedirect('index')
            response.set_cookie('username',username,max_age=3600)
            if user is not None and user.is_active:
                auth.login(request,user)
                return render_to_response('index.html',{'form':form,'password_is_wrong':True},context_instance=RequestContext(request))
            else:
                return render_to_response('login.html',{'form':form,'password_is_wrong':True},context_instance=RequestContext(request))
        else:
            return render_to_response('login.html',{'form':form,},context_instance=RequestContext(request))
"""查询php日志"""
@login_required(login_url='login')
@permission_required('auth.php',login_url='Nopri')
def SearchPhpLog(request):
    try:
        logpathlist = AddPhpLogpath.objects.all()
	print logpathlist
    except:
        write_log('can not find logpathlist')
	print 'logpathlist not exist'
    sql2 = 'select distinct(agent) from gameserverinfo'
    db = db_operate()
    try:
        agents = db.mysql_command(settings.LOGMANGER_MYSQL,sql2)
	print agents
    except:
        write_log('can not find agents')
	print 'agents not exist'
    AnsibleApiResult = ['show log:']
    if request.method == "POST":
        try:
            agent=request.POST['agent']
        except:
            write_log("can not get agent")
        try:
            logPath=request.POST['logdir']
        except:
            write_log('can not get logdir')
        try:
           logTime=request.POST['date']
        except:
            write_log('can not get logtime')
        try:
            serverId=request.POST['zone']
        except:
            write_log('can not get zone')
        try:
            logCount=request.POST['sum']
        except:
            write_log('can not get logCount')
    	timeArray = time.strptime(logTime,"%Y-%m-%d")
        otherStyleTime = time.strftime("%Y-%m-%d",timeArray)
        LogFile = "%s.txt" %(otherStyleTime)
    	try:
            serverIp = select_ip().selectip(agent,serverId)
        except:
            write_log('can not get serverIp')
        try:
            logexist = AddPhpLogpath.objects.all()
        except:
            write_log('can not get phppath')
	if logexist:
            for loglist in logexist:
                if logPath in loglist.logpath:
                    write_log('logpath is exist')
                else:
                    ll = AddPhpLogpath(logpath = logPath)
                    ll.save()
	else:
	    ll = AddPhpLogpath(logpath = logPath)
	    ll.save()
        serverIp = [serverIp]
        AnsibleModuleName = "shell"
        AnsibleInventory = ansible.inventory.Inventory(serverIp)
        AnsibleCommand = "tail -n %s /data/www/weblog/%s/%s/%s" %(logCount,agent,logPath,LogFile)
        try:
            AnsibleApiResult = (json.loads(AnsibleApi(AnsibleModuleName,AnsibleInventory,AnsibleCommand)))['msg']
	    if  not AnsibleApiResult:
	        AnsibleApiResult = '日志没有被发现，也就是没有的意思啦!!!'
	    print type(AnsibleApiResult)
#            write_log(AnsibleApiResult)
        except:
            write_log('ansible exec error')
    return render_to_response('SearchPhpLog.html',{'result':logpathlist,'result2':agents,'result3':str(AnsibleApiResult).encode('utf-8')},context_instance=RequestContext(request))
"""download php log"""
@login_required(login_url='login')
@permission_required('auth.php',login_url='Nopri')
def DownPhpLog(request):
    try:
        logpathlist = AddPhpLogpath.objects.all()
	print logpathlist
    except:
        write_log('can not find logpathlist')
	print 'logpathlist not exist'
    sql2 = 'select distinct(agent) from gameserverinfo'
    db = db_operate()
    try:
        agents = db.mysql_command(settings.LOGMANGER_MYSQL,sql2)
	print agents
    except:
        write_log('can not find agents')
	print 'agents not exist'
    AnsibleApiResult = ['show log:']
    linkaddress = 'link address'
    if request.method == "POST":
        try:
            agent=request.POST['agent']
        except:
            write_log("can not get agent")
        try:
            logPath=request.POST['logdir']
        except:
            write_log('can not get logdir')
        try:
           logTime=request.POST['date']
        except:
            write_log('can not get logtime')
        try:
            serverId=request.POST['zone']
        except:
            write_log('can not get zone')
        try:
            hour = request.POST['hour']
        except:
            write_log('can not get hour')
        hoursplit = splithour(hour)
	logFile = []
	curtime = getCurrentTime()
        for hourunit in hoursplit:
            logTime1 = logTime + '-' + hourunit
            timeArray = time.strptime(logTime1,"%Y-%m-%d")
            otherStyleTime = time.strftime("%Y-%m-%d",timeArray)
            LogFile = "%s.txt" %(otherStyleTime)
	    logFile.append(LogFile)

    	try:
            serverIp = select_ip().selectip(agent,serverId)
        except:
            write_log('can not get serverIp')
        try:
            logexist = AddPhpLogpath.objects.all()
        except:
            write_log('can not get phppath')
	if logexist:
            for loglist in logexist:
                if logPath in loglist.logpath:
                    write_log('logpath is exist')
		    print 'logpath is exist'
                else:
                    ll = AddPhpLogpath(logpath = logPath)
                    ll.save()
	else:
	    ll = AddPhpLogpath(logpath = logPath)
	    ll.save()
	
        linkaddress = 'http://%s/download/%s.phplog.%s.%s.tgz' % (serverIp,agent,serverId,curtime)
        serverIp = [serverIp]
        AnsibleModuleName = "shell"
        AnsibleInventory = ansible.inventory.Inventory(serverIp)
#	for LogFile in logFile:
#	    print LogFile
#	    file = LogFile + " "
#	    print file
#	    tarfile = '%s%s%s' % (agent,serverId,hour[0])
        AnsibleCommand = "cd /data/www/weblog/%s/%s  &&  tar  zvcf /data/www/download/%s.phplog.%s.%s.tgz  %s" %(agent,logPath,agent,serverId,curtime," ".join(logFile))
	    
#            AnsibleCommand = "cd /data/www/weblog/%s/%s  && mkdir %s &&  cp %s %s && tar  zvcf /data/www/download/%s.%s.%s.tgz  %s" %(agent,logPath,agent,LogFile,agent,agent,serverId,hour[0],agent)
	print AnsibleCommand
#	print AnsibleCommand
    	try:
            AnsibleApiResult = AnsibleApi(AnsibleModuleName,AnsibleInventory,AnsibleCommand)
	#    linkaddress = 'http://serverIp/download/%s.%s.%s.tgz' % (agent,serverId,hour[0]
#            write_log(AnsibleApiResult)
        except:
            write_log('ansible exec error')
#    linkaddress = 'http://serverIp/download/%s.%s.%s.tgz' % (agent,serverId,hour[0])
    print linkaddress
    return render_to_response('DownPhpLog.html',{'result':logpathlist,'result2':agents,'result3':linkaddress},context_instance=RequestContext(request))
"""search java log"""
@login_required(login_url='login')
@permission_required('auth.java',login_url='Nopri')
def ViewJavaLog(request):
    try:
        logpathlist = AddLogpath.objects.all()
    except:
        write_log('can not find logpathlist')
	print 'logpathlist not exist'
    sql2 = 'select distinct(agent) from gameserverinfo'
    db = db_operate()
    try:
        agents = db.mysql_command(settings.LOGMANGER_MYSQL,sql2)
    except:
        write_log('can not find agents')
    AnsibleApiResult = ['show log:']
    logname = 'QMRServerlog'

    if request.method == 'POST':
        try:
            agent=request.POST['agent']
        except:
            write_log("can not get agent")
        try:
            logPath=request.POST['logdir']
        except:
            write_log('can not get logdir')
        try:
            logfile = request.POST['logfile']
        except:
            write_log('can not get logfile')
        try:
           logTime=request.POST['date']
        except:
            write_log('can not get logtime')
        try:
            serverId=request.POST['zone']
        except:
            write_log('can not get zone')
        try:
            logAccount = request.POST['logAccount']
        except:
            write_log('can not get logAccount')
        
        timeArray = time.strptime(logTime,"%Y-%m-%d %H:%M:%S")
	
        basedir = '/data/game/qmrserver%s/qmrserver/' % (serverId)
        try:
            serverIp = select_ip().selectip(agent,serverId)
        except:
            write_log('can not get serverIp')
        try:
            queryset = AddLogpath.objects.values('logtype').filter(logpath=logPath)[0]['logtype']
        except:
            write_log('can not find queryset-logtype')
        try:
            logname = AddPhpLogpath.objects.values('logname')
            print logname
        except:
            write_log('can not find logname')
   # timeArray = time.strptime(logTime,"%Y-%m-%d %H:%M:%S")
#    basedir = '/data/game/qmrserver%s/qmrserver' % (serverId)
        if queryset == 'hour':
            otherStyleTime = time.strftime("%Y%m%d%H",timeArray)
            print otherStyleTime
            if time.strftime('%Y%m%d%H',time.localtime(time.time())) == otherStyleTime:
	        logName = basedir + logPath +  "/" + logfile + ".log" + "." + otherStyleTime
            else:
                logName = basedir + logPath +  "/" + logfile + ".log" + "." + otherStyleTime
        else:
            otherStyleTime = time.strftime("%Y%m%d",timeArray)
            print otherStyleTime
            if time.strftime('%Y%m%d',time.localtime(time.time())) == otherStyleTime:
                logName = basedir + logPath +  "/" + logfile + ".log" + "." + otherStyleTime
            else:
                logName = basedir + logPath +  "/" + logfile + ".log" + "." + otherStyleTime
        serverIp = [serverIp]
        AnsibleModuleName = "shell"
        AnsibleInventory = ansible.inventory.Inventory(serverIp)
        AnsibleCommand = "tail -n %s %s" %(logAccount,logName)
        write_log(AnsibleCommand)
        try:
            AnsibleApiResult = (json.loads(AnsibleApi(AnsibleModuleName,AnsibleInventory,AnsibleCommand)))['msg']
	    if not AnsibleApiResult:
                AnsibleApiResult = "日志没有被发现 也就是没有的意思那!!!"
#	    write_log(AnsibleApiResult)
        except:
            write_log('ansible command fail')

    return render_to_response('ViewJavaLog.html',{'result':logpathlist,'result2':agents,'result3':str(AnsibleApiResult).encode('utf-8')},context_instance=RequestContext(request))

"""download java log"""
@login_required(login_url='login')
@permission_required('auth.java',login_url='Nopri')
def DownJavaLog(request):
    try:
        logpathlist = AddLogpath.objects.all()
    except:
        write_log('can not find logpathlist')
	print 'logpathlist not exist'
    sql2 = 'select distinct(agent) from gameserverinfo'
    db = db_operate()
    try:
        agents = db.mysql_command(settings.LOGMANGER_MYSQL,sql2)
    except:
        write_log('can not find agents')
    AnsibleApiResult = ['show log:']
    logname = 'QMRServerlog'
    linkaddress = 'link address'
    curtime = getCurrentTime()
    if request.method == 'POST':
        try:
            agent=request.POST['agent']
        except:
            write_log("can not get agent")
        try:
            logPath=request.POST['logdir']
        except:
            write_log('can not get logdir')
        try:
            logfile = request.POST['logfile']
        except:
            write_log('can not get logfile')
        try:
           logTime=request.POST['date']
        except:
            write_log('can not get logtime')
        try:
            serverId=request.POST['zone']
        except:
            write_log('can not get zone')
        try:
            hour = request.POST['hour']
        except:
            write_log('can not get logAccount')
        hoursplit = splithour(hour)



        timeArray = time.strptime(logTime,"%Y-%m-%d %H:%M:%S")

        basedir = '/data/game/qmrserver%s/qmrserver/' % (serverId)
        try:
            serverIp = select_ip().selectip(agent,serverId)
        except:
            write_log('can not get serverIp')
        try:
            queryset = AddLogpath.objects.values('logtype').filter(logpath=logPath)[0]['logtype']
        except:
            write_log('can not find queryset-logtype')
        try:
            logname = AddPhpLogpath.objects.values('logname')
            print logname
        except:
            write_log('can not find logname')
   # timeArray = time.strptime(logTime,"%Y-%m-%d %H:%M:%S")
#    basedir = '/data/game/qmrserver%s/qmrserver' % (serverId)
        linkaddress = 'http://%s/download/%s.gamelog.%s.%s.tgz' % (serverIp,agent,serverId,curtime)
        logNamelist = []
        if queryset == 'hour':
            otherStyleTime = time.strftime("%Y%m%d",timeArray)
            for hour in hoursplit:
                otherStyleTimehour = otherStyleTime + hour
#                print otherStyleTime
                if time.strftime('%Y%m%d%H',time.localtime(time.time())) == otherStyleTimehour:
	                logName = logfile + ".log" + "." + otherStyleTimehour
                else:
                    logName = logfile + ".log" + "." + otherStyleTimehour
                    print logName
                logNamelist.append(logName)
	    logNamelist.append(logfile+'.log')
            print logNamelist
        else:
            otherStyleTime = time.strftime("%Y%m%d",timeArray)
            print otherStyleTime
            if time.strftime('%Y%m%d',time.localtime(time.time())) == otherStyleTime:
                logName = basedir + logPath +  "/" + logfile + ".log" + "." + otherStyleTime
            else:
                logName = basedir + logPath +  "/" + logfile + ".log" + "." + otherStyleTime
            logNamelist.append(logName)
	print logNamelist
        serverIp = [serverIp]
        AnsibleModuleName = "shell"
        AnsibleInventory = ansible.inventory.Inventory(serverIp)
        AnsibleCommand = "cd /data/game/qmrserver%s/qmrserver/%s  &&  tar  zvcf /data/www/download/%s.gamelog.%s.%s.tgz  %s" %(serverId,logPath,agent,serverId,curtime," ".join(logNamelist))
        write_log(AnsibleCommand)
        try:
            AnsibleApiResult = AnsibleApi(AnsibleModuleName,AnsibleInventory,AnsibleCommand)
#	    write_log(AnsibleApiResult)
        except:
            write_log('ansible command fail')
#    linkaddress = 'http://%s/download/%s.%s.game.%s.tgz' % (serverIp,agent,serverId,hour[0])
    return render_to_response('DownJavaLog.html',{'result':logpathlist,'result2':agents,'result3':linkaddress},context_instance=RequestContext(request))
"""add log path"""
@csrf_exempt
def test(request):
    """add java logpath"""
    response_data = {}  
#    response_data['result'] = 'ok'  
    try:
        response_data['data'] = request.POST['url']
        write_log(request.POST['url'])
    except:
        write_log('can not get url')
    response_data['logname'] = request.POST['logname']
    response_data['data1'] = request.POST['type']
    print 'get response_data'
    print response_data
    logexist = AddLogpath.objects.all()

    for list in logexist:
	print list.logpath
    if request.POST['url'] in list.logpath:
	print 'the logpath is exist'
    else:
	l1 = AddLogpath(logpath=request.POST['url'],logname=request.POST['logname'],logtype=request.POST['type'])
	l1.save()
    result = "chenggong"
#    return HttpResponse('result')
    return HttpResponse(json.dumps(response_data['data']), content_type="application/json")
