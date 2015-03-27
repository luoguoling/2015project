__author__ = 'Administrator'
import ansible.runner
import ansible.inventory
import json
def AnsibleApi(AnsibleModuleName,AnsibleInventory,AnsibleCommand):
    ReturnMsg = {}
    runner = ansible.runner.Runner(
#	remote_user = username,
        module_name = AnsibleModuleName,
        inventory = AnsibleInventory,
        module_args = AnsibleCommand,
        environment = {'LANG':'zh_CN.UTF-8','LC_CTYPE':'zh_CN.UTF-8'},
    )
    ReturnValue = runner.run()
    print ReturnValue
    if ReturnValue is None:
        ReturnMsg['code'] = "-1"
        ReturnMsg['msg'] = "hosts not found"
    for (hostname,result) in ReturnValue['contacted'].items():
        if result['rc'] == "0":
            ReturnMsg['code'] = "0"
            ReturnMsg['msg'] = result['stdout']
	elif result['rc'] == "1":
	    ReturnMsg['code'] = "1"
	    ReturnMsg['msg'] = "no files"
        else:
            ReturnMsg['code'] = str(result['rc'])
            ReturnMsg['msg'] = result['stdout']
    for (hostname,result) in ReturnValue['dark'].items():
        ReturnMsg['code'] = "-3"
        ReturnMsg['msg'] = result
    return json.dumps(ReturnMsg)
