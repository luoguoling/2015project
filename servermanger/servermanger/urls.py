from django.conf.urls import patterns, include, url
import xadmin
from django.contrib import admin
xadmin.autodiscover()
admin.autodiscover()
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'servermanger.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'xadmin/',include(xadmin.site.urls),name='xadmin'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/','logmanger.views.login',name='login'),
    url(r'^SearchPhpLog/','logmanger.views.SearchPhpLog',name='SearchPhpLog'),
    url(r'^DownPhpLog/','logmanger.views.DownPhpLog',name='DownPhpLog')
)
