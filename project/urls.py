from django.conf.urls import patterns
from mis import views
from views import excelfile
from views import more
from views import message_dao
from views import option_dao
from views import file_dao
import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_PATH, 'show_indexes':True}),
        (r'^message/$',views.message),
        (r'^tree/$',views.submit),
        (r'^test/$',views.test),
        (r'^base/$',views.base),
        (r'^getMessage/$',message_dao.getMessage),
        (r'^setMessage/$',message_dao.setMessage),
        (r'^newmessage/$',message_dao.newMessage),
        (r'^test2/$',views.test2),
        (r'^AjaxSearchOrgan/$',message_dao.AjaxSearchOrgan),
        (r'^UpdateMessage/$',message_dao.UpdateMessage),
        (r'^setDefaultUser/$',views.setDefaultUser),
        (r'^ShowFileList/$',file_dao.GetFileList),
        (r'^DeleteFile/$',file_dao.DeleteFile),
        (r'^DownLoad/$',file_dao.ReadFile),
        (r'^excelfile/$',excelfile.excel_request),
        (r'^test3/$',excelfile.test),
        (r'^uploadtest/$',more.upload_file),
        (r'^getOrganList/$',message_dao.GetOrganList),
        (r'^OrganIndex/$',message_dao.OranIndex),
        (r'^OrganNextIndex/$',message_dao.OrganNextIndex),
        (r'^RemoveOrgan/$',message_dao.RemoveOrgan),
        (r'^getNextOrgan/$',message_dao.GetNextOrgans),
        (r'^CreateNewMessage/$',message_dao.CreateNewMessage),
        (r'^GetOptionList/$',option_dao.GetOptionList),
        (r'^AddOption/$',option_dao.AddOption),
        (r'^DelOption/$',option_dao.DelOption),
        (r'^SearchOrganList/$',message_dao.SearchOrganList),


        #####
        (r'^vpn/$',message_dao.getVPN),
        (r'^autoIP/$',message_dao.tunnel_ip),
        #####
                       )
