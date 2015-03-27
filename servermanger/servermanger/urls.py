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
    url(r'^DownPhpLog/','logmanger.views.DownPhpLog',name='DownPhpLog'),
    url(r'^test/','logmanger.views.test',name='test'),
    url(r'^ViewJavaLog/','logmanger.views.ViewJavaLog',name='ViewJavaLog'),
    url(r'^DownJavaLog/','logmanger.views.DownJavaLog',name='DownJavaLog'),
    url(r'^Nopri/','logmanger.views.Nopri',name='Nopri'),
    #about updatemanger
    url(r'^get_tree_data','updatemanger.views.JSONGetView',name='get_tree_data'),
    url(r'^set_tree','updatemanger.views.JSONSetView',name='set_tree'),
    url(r'^viewztree','updatemanger.views.ViewZtree',name='viewztree'),
    url(r'^updatejava','updatemanger.views.updatejava',name='updatejava')

)
