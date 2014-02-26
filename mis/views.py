# Create your views here.
#coding=utf-8
import os
import json
import string
import random
import sys
import time
import uuid

from datetime import *
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
import xlrd
import pymongo

from project import settings
from mis.models import *
from django.core.paginator import Paginator



def setDefaultUser(request):
    """
    初始化账号密码
    """
    db=connection()
    obj=db['user']
    json={
        "name":"admin",
        "password":"123"
    }
    obj.save(json)
    return  HttpResponse("ok")

def test(request):
    d=uuid.uuid4()
    return render_to_response("test.html",locals())

def submit(request):

    return render_to_response("tree/submit.html")

@csrf_exempt
def test2(request):
    SaveFile(request.FILES['file'],"a","static")
    return HttpResponse()

@csrf_exempt
def ReadFile(request):
    """
    下载文件
    """
    id=request.GET.get("id")
    name=request.GET.get("name")
    file_name = "static/files/"+id+"/"+name
    c=open(file_name,"rb").read()
    response = HttpResponse(c,mimetype='text/plain')
    response['Content-Disposition'] = 'attachment; filename='+name
    return response

def SaveFile(file):
    """
    上传文件
    """
    dir="static"
    filename=uuid.uuid4().__str__()
    name=file.name
    str=name.split(".")[1]

    with open(dir+'/'+filename+'.'+str,'wb+') as path:
        for chunk in file.chunks():
            path.write(chunk)
    return None

@csrf_exempt
def DeleteFile(request):
    """
    :前端根据文件名与机构ID删除对应文件
    """
    if request.method == 'POST':
        try:
            filename=request.POST.get('filename')
            id=request.POST.get('id')
            path='static/files/'+id+'/'+filename
            os.remove(path)
            return HttpResponse("ok")
        except:
            return HttpResponse("error")


#SearchMessage
@csrf_exempt
def message(request):
    """
    访问MongoDB
    :根据机构ID获取相应信息
    """
    id=request.POST.get("id")
    name=request.POST.get("name")
    to=request.POST.get("to")
    db=connection()
    obj=db["wens"]


    try:
        cursor=obj.find({"ID":id})[0]
        pathID=cursor['ID']
        d='static/files/'+pathID+'/'
        files=os.listdir(d)

        if to=='set':
            return render_to_response("message/setMessage.html",locals())
        else:
            return render_to_response("message/getMessage.html",locals())
    except:
        return  render_to_response("message/ToNewMessage.html",locals())

#Get Connection
def connection():
    connection=pymongo.Connection('localhost',27017)
    db=connection.test
    return db




#Get message from template and save
@csrf_exempt
def getMessage(request):
        """
        获取发送数据
        对信息进行删除修改
        """
        db=connection()
        myid=request.POST.get("myid")
        obj=db["wens"]
        obj.remove({"ID":myid })
        randomkey=request.POST.get('ike_preshare_key')

        #生成随机码
        if(randomkey=="" or randomkey is None):
            randomkey=randomKey()
        dir='static/files/'+request.POST.get('id')

        #判断dir存在并创建
        if not os.path.exists(dir):
            os.mkdir(dir)


        json={
            "name":request.POST.get("name"),
            "first":request.POST.get("first"),
            "second":request.POST.get('second'),
            "third":request.POST.get('third'),
            "ID":request.POST.get('id'),
            "operator":request.POST.get('operator'),
            "circuit":request.POST.get('circuit'),
            "downlinkBandwidth":request.POST.get('downlinkBandwidth'),
            "uplinkBandwidth":request.POST.get('uplinkBandwidth') ,
            "PublicIP":request.POST.get('PublicIP'),
            "PublicGATEWAY":request.POST.get('PublicGATEWAY'),
            "DNS":request.POST.get('DNS'),
            "IAD":request.POST.get("IAD"),
            "networkSupervisor":request.POST.get("networkSupervisor"),
            "intranetDiagram":IPSort(request.POST.getlist("Diagram",[])),
            "intranetGATEWAY":IPSort(request.POST.getlist("GATEWAY",[])),
            "deviceDiagram":request.POST.get("deviceDiagram"),
            "deviceManagement":request.POST.get("deviceManagement"),
            "LoopbackIP":request.POST.get("LookbackIP"),
            "deviceService":",".join(request.POST.getlist("deviceService",[])),
            "peerID":request.POST.get("peerID"),
            "Tunnel0":request.POST.get("Tunnel0"),
            "Tunnel1":request.POST.get("Tunnel1"),
            "grekey":request.POST.get("grekey"),
            "ike_preshare_key":randomkey,
            "terminalIkePeer":request.POST.get("terminalIkePeer"),
            "centerTunnel":request.POST.get("centerTunnel"),
            "centerTemplate":request.POST.get("centerTemplate"),
            "centerNQA":request.POST.get("centerNQA"),
            "username":request.POST.get("username"),
            "currentPassword":request.POST.get("currentPassword"),
            "historicalPassword":request.POST.get("historicalPassword"),
            "currentSSH":request.POST.get("currentSSH"),
            "historicalSSH":request.POST.get("historicalSSH"),
            "nat":request.POST.get("nat"),
            "note":
                request.POST.getlist("note",[]),
            # "config":request.POST.get("config")
        }
        filename=request.POST.get("filename")
        #对上传文件进行保存
        file=request.FILES.get('config')
        if file is not None:
            SaveFile(file,filename,dir)
        obj.save(json)
        request.session['to']='set'
        return HttpResponseRedirect("/main/?id="+myid,locals())



def reback(request):
    db=connection()
    obj=db['wens']
    json={
        'name':'bb',
        "first":"ss",
        "second":"稔村公司",
        "third":"太平公司",
        "ID":"WSRCTPTPZJC",
        "operator":"",
        "circuit":"",
        "downlinkBandwidth":"",
        "uplinkBandwidth":"" ,
        "PublicIP":"",
        "PublicGATEWAY":"",
        "DNS":"",
        "IAD":"",
        "networkSupervisor":"",
        "intranetDiagram":['a','b','c'],
        "intranetGATEWAY":['a','b','c'],
        "deviceDiagram":"",
        "deviceManagement":"",
        "LookbackIP":"",
        "deviceService":[
            "snmp",
            "https",
            "telnet",
        ],
        "peerID":"",
        "Tunnel0":"",
        "Tunnel1":"",
        "grekey":"",
        "ike_preshare_key":"",
        "terminalIkePeer":"",
        "centerTunnel":r"",
        "centerTemplate":"",
        "centerNQA":"",
        "username":"",
        "currentPassword":"",
        "historicalPassword":"",
        "currentSSH":"",
        "historicalSSH":"",
        "nat":"",
        "note":
            ['a','b','c'],
        "config":""
        }
    obj.save(json)
    request.session['to']='set'
    test=request.session.get('to')
    return HttpResponse(test)

#make randomkey
def randomKey():
    """
    :生成16位随机数
    ：区分大小写
    """
    s=""
    str=string.letters+string.digits
    str=random.sample(str,16)
    for i in range(0,16):
        s=str[i]+s
    return s



#redirect to template
def main(request):
    id=request.GET.get("id")
    path=settings.HERE+"/wens.json"
    f=open(path)
    jso=f.read().decode("gbk").encode("utf-8")
    dump=json.loads(jso)
    return  render_to_response("main.html",locals())



@csrf_exempt
def login(request):
    name=request.POST.get("username")
    password=request.POST.get("password")
    try:
        user=User.objects.get(name=name,password=password)
        if user is not None:
            return HttpResponseRedirect("/main/")
    except:
        return render_to_response("LoginIn.html.html")


#search by id
@csrf_exempt
def SearchById(request):
    """
    根据机构ID搜索数据
    """
    db=connection()
    obj=db['wens']
    id=request.POST.get('id')
    try:
        cursor=obj.find({"ID":{"$regex":id } })[0]
        return render_to_response("message/getMessage.html",locals())
    except:

        return HttpResponse("暂无信息")

#search by name
@csrf_exempt
def SearchByName(request):
    """
    :根据机构名称搜索数据
    :
    """
    db=connection()
    obj=db['wens']
    name=request.POST.get('name')
    try:
        cursor=obj.find({"name":{"$regex": name }})[0]
        return render_to_response("message/getMessage.html",locals())
    except:
        return render_to_response("message/ToNewMessage.html",locals())

def index(request):
    if(request.session.get('user') is not None):
        return HttpResponseRedirect("/main/")
    return render_to_response("LoginIn.html",locals())

def Exit(request):
    request.session.clear()
    return render_to_response("LoginIn.html")

@csrf_exempt
def newMessage(request):
    id=request.POST.get("id")
    name=request.POST.get("name")
    return render_to_response("message/newMessage.html",locals())

def IPSort(list):
    """
    :IP段解析排序
    """
    array=[]
    for i in list:
        if(i != "" and i != None):
            array.append(IPSplit(i))
    if(array.__len__()==1):
        print array.__len__()
        return array
    elif(array.__len__()==0):
        print array.__len__()
        array.append("")
        return array
    for i in range(1,len(array)):
        for j in range(0,len(array)-i):
            a=array[j].split(".")
            b=array[j+1].split(".")
            for k in range(4):
                if(string.atoi(a[k])<string.atoi(b[k])):
                    break;
                elif(string.atoi(a[k])>string.atoi(b[k])):
                    replace=array[j]
                    array[j]=array[j+1]
                    array[j+1]=replace
                    break;
    return array


def IPSplit(ip):
    str=ip.replace("\\","/").split("/")[0]
    return str

    # transform excel to json
def excel(request):
        """

        :param request:
        :return:
        """
        reload(sys)
        sys.setdefaultencoding('gbk')
        data=xlrd.open_workbook("f://ch8/work.xls")
        table=data.sheets()[0]
        colnum=table.nrows
        root={}
        obj={}
        first={}
        secarr=[]
        secobj={}
        thiarr=[]
        thiobj={}
        forarr=[]
        forobj={}
        fifarr=[]
        fifobj={}
        level=0
        check=0
        for i in range(2,1002):
            object={}
            col=table.row_values(i)
            object.__setitem__("name",col[0])
            object.__setitem__("id",col[1])
            level=col[2]
            if(level!=check):
                if(check<level):
                    if(level==2):
                        first.__setitem__("second",secarr)
                    elif(level==3):
                        thiarr=[]
                        secobj.__setitem__("third",thiarr)
                    elif(level==4):
                        forarr=[]
                        thiobj.__setitem__("forth",forarr)
                    elif(level==5):
                        fifarr=[]
                        forobj.__setitem__("fifth",fifarr)
                check=level
            if(level==2):
                secarr.append(object)
                secobj=object
            elif(level==3):
                thiarr.append(object)
                thiobj=object
            elif(level==4):
                forarr.append(object)
                forobj=object
            elif(level==5):
                fifarr.append(object)
                fifobj=object
        first.__setitem__("name","温氏集团")
        first.__setitem__("id","WS")
        dump=json.dumps(first,encoding="UTF-8", ensure_ascii=False)
        f=open("f://ch8/wens.json")
        a=""
        while 1:
            line=f.readline()
            if not line:
                break
            a=a+line
        return render_to_response("test.html",locals())

def base(request):
    return render_to_response("base.html")



