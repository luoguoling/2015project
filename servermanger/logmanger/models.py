from django.db import models

# Create your models here.
from django.db import models
from django.contrib import admin
# Create your models here.
class AddLogpath(models.Model):
	logpath = models.CharField(max_length=500)
	logname = models.CharField(max_length=100)
        logtype = models.CharField(max_length=50)
        def __unicode__(self):
            return self.logpath
class AddPhpLogpath(models.Model):
    logpath = models.CharField(max_length=500,default='rmblog')
    def __unicode__(self):
        return self.logpath
class ExecCommand(models.Model):
    execcommand = models.CharField(max_length=100)
class addCommand(models.Model):
    addcommand = models.CharField(max_length=100)
    def __unicode__(self):
        return self.addcommand

