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
from servermanger import settings
from django.contrib.auth import authenticate,login
from logmanger.forms import LoginForm
from django.contrib.auth.decorators import login_required,permission_required
"""main"""
#@login_required(login_url='login')
def index(request):
    return render_to_response('index.html')
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
                return render_to_response('DownPhpLog.html',{'form':form,'password_is_wrong':True},context_instance=RequestContext(request))
            else:
                return render_to_response('login.html',{'form':form,'password_is_wrong':True},context_instance=RequestContext(request))
        else:
            return render_to_response('login.html',{'form':form,},context_instance=RequestContext(request))
"""查询php日志"""
@login_required(login_url='login')
@permission_required('auth.php',login_url='login')
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
	    print logexist
        except:
            write_log('can not get phppath')
	if logexist:
            for loglist in logexist:
                if loglist.logpath == logPath:
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
            AnsibleApiResult = AnsibleApi(AnsibleModuleName,AnsibleInventory,AnsibleCommand)
	    print type(AnsibleApiResult)
            write_log(AnsibleApiResult)
        except:
            write_log('ansible exec error')
    return render_to_response('SearchPhpLog.html',{'result':logpathlist,'result2':agents,'result3':AnsibleApiResult},context_instance=RequestContext(request))
"""download php log"""
@login_required(login_url='login')
@permission_required('auth.php',login_url='login')
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
        hour = splithour(hour)
        for hour in hour:
            logTime1 = logTime + hour
            timeArray = time.strptime(logTime1,"%Y-%m-%d")
            otherStyleTime = time.strftime("%Y-%m-%d",timeArray)
            LogFile = "%s.txt" %(otherStyleTime)
    	try:
            serverIp = select_ip().selectip(agent,serverId)
        except:
            write_log('can not get serverIp')
        try:
            logexist = AddPhpLogpath.objects.all()
	    print logexist
        except:
            write_log('can not get phppath')
	if logexist:
            for loglist in logexist:
                if loglist.logpath == logPath:
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
    AnsibleCommand = "tar  zvcf %s.%s.tar.gz /data/www/weblog/%s/%s/%s" %(agent,hour[0],agent,logPath,LogFile)
    try:
        AnsibleApiResult = AnsibleApi(AnsibleModuleName,AnsibleInventory,AnsibleCommand)

        write_log(AnsibleApiResult)
    except:
        write_log('ansible exec error')
    linkaddress = "http://%s/download/%s.%s.tar.gz" %(serverIp,agent,hour[0])
    return render_to_response('DownPhpLog.html',{'result':logpathlist,'result2':agents,'result3':linkaddress},context_instance=RequestContext(request))
"""search java log"""
@login_required(login_url='login')
@permission_required('auth.php',login_url='login')
def SearchJavaLog(request):
    pass
"""download java log"""
@login_required(login_url='login')
@permission_required('auth.php',login_url='login')
def DownJavaLog(request):
    pass

