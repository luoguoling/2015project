__author__ = 'Administrator'
from django.contrib import admin
import xadmin
# Register your models here.
from logmanger.models import addCommand
from logmanger.models import AddLogpath
from logmanger.models import AddPhpLogpath
class logAdmin(object):
    search_fileds=('')
xadmin.site.register(addCommand,logAdmin)
xadmin.site.register(AddLogpath,logAdmin)
xadmin.site.register(AddPhpLogpath,logAdmin)


