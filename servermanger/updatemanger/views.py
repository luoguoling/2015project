#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
#rom updateapp.models import serverlist
from servermanger.mysql import db_operate
from servermanger.servers import serverinfo
from servermanger.AnsibleApi import AnsibleApi
import ansible.runner,ansible.inventory
from servermanger.writelog import write_log
import json
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
@csrf_exempt
def JSONGetView(request):
    server = serverinfo()
    servers = server.serverinfo()
    agents = server.agentsinfo()
    
#   servers = serverlist.objects.values('id','agent','serverId','ipaddress').order_by('serverId')
#   agents = serverlist.objects.values('agent').distinct().order_by('agent')
#   serverIp = select_ip().selectip(agent,serverId)
    id = {}
    offset = 100000
    tree_list = []
#    print servers,agents
    for i,agent in enumerate(agents):
#        print i,agent
        id[agent['agent']] = offset + int(i)
        print id
    for key,value in id.items():
        serveragent = {}
        serveragent['zone'] = key
        serveragent['id'] = value
        serveragent['agent'] = 'noagent'
        if serveragent not in tree_list:
            tree_list.append(serveragent)
    for server in servers:
        for key,value in id.items():
            if server['agent'] == key:
                server['parentId'] = value
                if server not in tree_list:
                    tree_list.append(server)
    result = json.dumps(tree_list)
    print 'result is....'
    return HttpResponse(result,content_type="application/json")
@csrf_exempt
def JSONSetView(request):
    response_data = {}
    json_tree = request.POST.get('jsonTree')
    tree_change_nodes = json.loads(json_tree)
    tree_list = []
    for i in tree_change_nodes[1:]:
        newdic = {}
        for n in i.keys():
            if 'noagent' not in i['agent']:
                newdic['agent'] = i['agent']
                newdic['zone'] = i['zone']
                if newdic not in tree_list:
                    tree_list.append(newdic)
    #for tt in tree_list:
    #    ip = serverlist.objects.values('ipaddress').filter(agent=tt['agent'],zone=tt['zone'])
     #   print ip
    return HttpResponse('ip',content_type="application/json")
@csrf_exempt
def ViewZtree(request):
    return render_to_response('checkbox.html')
@csrf_exempt
def updatejava(request):
    json_tree = request.POST.get('jsonTree')
    print 'json_tree is ..'
#    print json_tree
    tree_list = []
    try:
        tree_change_nodes = json.loads(json_tree)
#        print tree_change_nodes
#        tree_list = []
        for i in tree_change_nodes[1:]:
            newdic = {}
            for n in i.keys():
                if 'noagent' not in i['agent']:
                    newdic['agent'] = i['agent']
                    newdic['zone'] = i['zone']
                    newdic['ip'] = i['ip']
                    newdic['gamedata'] = i['gamedatadbname']
                    newdic['javadir'] = i['javadir']
                    if newdic not in tree_list:
                        tree_list.append(newdic)
    except:
        pass
	#print tree_list
    for tt in tree_list:
        print tt['agent'],tt['zone'],tt['ip'],tt['gamedata'],tt['javadir']
        serverIp = [tt['ip']]
        ip = serverIp[0]
        AnsibleModuleName = "synchronize"
        AnsibleInventory = ansible.inventory.Inventory(serverIp)
        AnsibleCommand = "src=/var/ftp/qmrserver/ dest=%s" % tt['javadir']
        try:
             AnsibleApiResult = json.loads(AnsibleApi(AnsibleModuleName,AnsibleInventory,AnsibleCommand))
                #print ip

#             ExecResult =  AnsibleApiResult['contacted']['%s' % ip]['rc']
#             print ExecResult
                #if not AnsibleApiResult:
                 #   AnsibleApiResult = 'not exec success'
        except:
            write_log('ansible exception')

     #       ip = serverlist.objects.values('ipaddress').filter(agent=tt['agent'],zone=tt['zone'])

    return render_to_response('updatejava.html')
