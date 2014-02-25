#coding=utf-8
import os
import json
import string
import random
import sys

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
import xlrd
import pymongo

from project import settings
from mis.models import *


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

def connection():
    connection=pymongo.Connection('localhost',27017)
    db=connection.test
    return db

def SaveFile(file,filename,dir):
    """
    上传文件
    """
    name=file.name
    str=name.split(".")[1]
    with open(dir+'/'+filename+'.'+str,'wb+') as path:
        for chunk in file.chunks():
            path.write(chunk)
    return None



#获取指定层级公司数据
@csrf_exempt
def GetOrganList(request):
    rank=request.POST.get("rank")
    rank="2"
    organs=GetRank(rank).all()
    return render_to_response("message/OrganList.html",locals())

#获取指定层级下级公司数据
@csrf_exempt
def GetNextOrgans(request):
    id=request.POST.get("id")
    rank=request.POST.get("rank")
    print id,rank
    organs=GetNextRank(id,rank)
    return render_to_response("message/OrganList.html",locals())

#新建选项
def CreateAbstractField(request):
    type=request.POST.get("type")
    name=request.POST.get("name")
    Abstraction.objects.bulk_create([Abstraction(name=name,type=type)])
    return render_to_response()

#获取选项列表
def GetAbstractField(request):
    type=request.POST.get("type")
    fields=Abstraction.objects.filter(type=type)
    return render_to_response()

#创建自定义栏目
def CreateExtraField(request):
    name=request.POST.get("name")
    ExtraField.objects.create()


def SaveOrUpdateMessage(request,method):
    """
    新增或更新机构信息集中实现
    """

    name=request.POST.get("department")
    organid=request.POST.get('organid')
    operator=request.POST.get('operator')
    circuit=request.POST.get('circuit')
    downlinkBandwidth=request.POST.get('downlinkBandwidth')
    uplinkBandwidth=request.POST.get('uplinkBandwidth')
    PublicIP=request.POST.get('PublicIP')
    PublicGATEWAY=request.POST.get('PublicGATEWAY')
    DNS=request.POST.get('DNS')
    IAD=request.POST.get("IAD")
    networkSupervisor=request.POST.get("networkSupervisor")
    networkSupervisorIP=request.POST.get("networkSupervisorIP")
    intranetDiagram=json.dumps(request.POST.getlist("Diagram",[]))
    intranetGATEWAY=json.dumps(request.POST.getlist("GATEWAY",[]))
    deviceDiagram=request.POST.get("deviceDiagram")
    deviceManagement=request.POST.get("deviceManagement")
    LoopbackIP=request.POST.get("LoopbackIP")
    deviceService=json.dumps(request.POST.getlist("deviceService",[]))
    peerID=request.POST.get("peerID")
    Tunnel0=request.POST.get("Tunnel0")
    Tunnel1=request.POST.get("Tunnel1")
    grekey=request.POST.get("grekey")

    ike_preshare_key = jia_mi(request)

    terminalIkePeer=request.POST.get("terminalIkePeer")
    centerTunnel=request.POST.get("centerTunnel")
    centerTemplate=request.POST.get("centerTemplate")
    centerNQA=request.POST.get("centerNQA")
    username=request.POST.get("username")
    currentPassword=request.POST.get("currentPassword")
    historicalPassword=request.POST.get("historicalPassword")
    currentSSH=request.POST.get("currentSSH")
    historicalSSH=request.POST.get("historicalSSH")
    nat=request.POST.get("nat")
    note=request.POST.getlist("note",[])
    parentID=request.POST.get("parentID")
    parentrRank=request.POST.get("parentRank")

    if method is "save":
        rank=request.POST.get("rank")


        mes=Message.objects.create()
        mes.rank=rank
        if rank =="3" and parentrRank == "2.5":
            obj=ThiRank.objects.create()
            preobj=GetRank(parentrRank).get(id=parentID)
            obj.parent_rank_half=preobj
        else:
            obj=GetRank(rank).create()
        if rank != "2" and rank !="3":
            preobj=GetRank(parentrRank).get(id=parentID)
            obj.parent_rank=preobj
        obj.organizeid=organid
        obj.name=name
        obj.message=mes
        obj.save()
    else:
        id=request.POST.get("id")
        mes=Message.objects.get(id=id)

    mes.name=name
    mes.organizeid=organid
    mes.operator=operator
    mes.circuit=circuit
    mes.downlinkBandwidth=downlinkBandwidth
    mes.uplinkBandwidth=uplinkBandwidth
    mes.PublicIP=PublicIP
    mes.PublicGATEWAY=PublicGATEWAY
    mes.DNS=DNS
    mes.IAD=IAD
    mes.networkSupervisor=networkSupervisor
    mes.networkSupervisorIP=networkSupervisorIP
    mes.intranetDiagram=intranetDiagram
    mes.intranetGATEWAY=intranetGATEWAY
    mes.deviceDiagram=deviceDiagram
    mes.deviceManagement=deviceManagement
    mes.LoopBackIP=LoopbackIP
    mes.deviceService=deviceService
    mes.peerID=peerID
    mes.Tunnel0=Tunnel0
    mes.Tunnel1=Tunnel1
    mes.grekey=grekey

    mes.ike_preshare_key=ike_preshare_key

    mes.terminalIkePeer=terminalIkePeer
    mes.centerTunnel=centerTunnel
    mes.centerTemplate=centerTemplate
    mes.centerNQA=centerNQA
    mes.username=username
    mes.currentPassword=currentPassword
    mes.historicalPassword=historicalPassword
    mes.currentSSH=currentSSH
    mes.historicalSSH=historicalSSH
    mes.nat=nat

    mes.save()


@csrf_exempt
def CreateNewMessage(request):
    """
    创建新机构接口
    """

    SaveOrUpdateMessage(request,"save")

    return HttpResponseRedirect("/OrganIndex/")



@csrf_exempt
def UpdateMessage(request):
    """
    更新机构信息接口
    """
    parentID=request.POST.get("parentID")
    parentrRank=request.POST.get("parentRank")
    id=request.POST.get("id")
    SaveOrUpdateMessage(request,"update")
    strr="修改成功！";
    path="/setMessage/?id="+id+"&rankid="+parentID+"&rank="+parentrRank

    return render_to_response("hint.html",locals())

def getMessage(request):
    """
    获取机构信息
    """
    rank=request.GET.get("rank")
    rankid=request.GET.get("rankid")
    id=request.GET.get("id")
    jd=json.JSONDecoder()
    obj=GetRank(rank).get(id=rankid)
    if rank=="3":
        if obj.parent_rank is not None:
            obj=obj.parent_rank
        else:
            obj=obj.parent_rank_half
    elif rank != "2":
        obj=obj.parent_rank
    cursor=Message.objects.get(id=id)
    cursor.intranetDiagram=jd.decode(cursor.intranetDiagram)
    cursor.intranetGATEWAY=jd.decode(cursor.intranetGATEWAY)
    cursor.deviceService=jd.decode(cursor.deviceService)
    return render_to_response("message/getMessage.html",locals())

def setMessage(request):
    """
    获取修改机构信息
    """
    rank=request.GET.get("rank")
    rankid=request.GET.get("rankid")
    id=request.GET.get("id")
    jd=json.JSONDecoder()
    obj=GetRank(rank).get(id=rankid)
    if rank=="3":
        if obj.parent_rank is not None:
            obj=obj.parent_rank
        else:
            obj=obj.parent_rank_half
    elif rank != "2":
        obj=obj.parent_rank
    elif rank == "2":
        obj.name="温氏集团"
    cursor=Message.objects.get(id=id)
    option1=Abstraction.objects.filter(type=1)
    option2=Abstraction.objects.filter(type=2)
    option3=Abstraction.objects.filter(type=3)
    cursor.intranetDiagram=jd.decode(cursor.intranetDiagram)
    cursor.intranetGATEWAY=jd.decode(cursor.intranetGATEWAY)
    cursor.deviceService=jd.decode(cursor.deviceService)
    return render_to_response("message/setMessage.html",locals())


def OranIndex(request):
    """
    按层级获取机构列表
    """
    rank=request.GET.get("rank")
    if rank is None:
        return render_to_response("message/OrganIndex.html",locals())
    organs=GetRank(rank).all()
    return render_to_response("message/OrganIndex.html",locals())

def OrganNextIndex(request):
    """
    获取下级列表
    """
    id=request.GET.get("id")
    rank=request.GET.get("rank")
    organs=GetNextRank(id,rank)
    return render_to_response("message/OrganIndex.html",locals())

def RemoveOrgan(request):
    """
    移除机构
    """
    id=request.GET.get("id")
    rank=request.GET.get("rank")
    obj=GetRank(rank).get(id=id)
    obj.delete()
    return HttpResponseRedirect("/OrganIndex/?rank="+rank)

def GetRank(rank):
    """
    返回层级实体对象实现
    """
    if rank == "2":
        obj=SecRank.objects
    elif rank == "2.5":
        obj=SecHalfRank.objects
    elif rank =="3":
        obj=ThiRank.objects
    elif rank == "4":
        obj=FouRank.objects
    return obj

def GetNextRank(id,rank):
    """
    返回下级列表实现
    """
    organs=[]
    if rank == "2":
        organ=SecRank.objects.get(id=id)
        sechalf=organ.sechalfrank_set.all()
        tri=organ.thirank_set.all()
        organs.extend(sechalf)
        organs.extend(tri)
    elif rank == "2.5":
        organ=SecHalfRank.objects.get(id=id)
        tri=organ.thirank_set.all()
        organs.extend(tri)
    elif rank == "3":
        organ=ThiRank.objects.get(id=id)
        tri=organ.fourank_set.all()
        organs.extend(tri)
    elif rank == "4":
        organ=FouRank.objects.get(id=id)
    return organs

@csrf_exempt
def SearchOrganList(request):
    name=request.POST.get("name")
    if name is None:
        return render_to_response("message/SearchOrgan.html",locals())
    organs=Message.objects.filter(name__contains=name)
    return render_to_response("message/SearchOrgan.html",locals())




#-------------------------------------------------分割线--------------------------------------
#vpn的创建
import codecs
import re

def createVPN(cursor):
    '''
        message = {}
    message["名字"] = cursor.peerID
    message["密码"] = cursor.currentPassword
    message["密钥key"] = cursor.ike_preshare_key
    message["公网ip"] = cursor.PublicIP
    message["公网网关"] = cursor.PublicGATEWAY
    message["内网段"] = cursor.intranetDiagram
    message["域名服务器1"] = cursor.DNS
    message["域名服务器2"] = cursor.DNS
    message["公网掩码"] = cursor.DNS
    message["隧道0"] = cursor.Tunnel0
    message["隧道1"] = cursor.Tunnel1
    message["密钥"] = cursor.grekey
    '''
    message = {}
    message["<1>"] = cursor.peerID
    message["<2>"] = cursor.currentPassword
    message["<3>"] = cursor.ike_preshare_key
    message["<4>"] = cursor.PublicIP
    message["<5>"] = cursor.PublicGATEWAY
    message["<6>"] = cursor.intranetDiagram
    message["<7>"] = cursor.DNS
    message["<8>"] = cursor.DNS
    message["<9>"] = cursor.DNS
    message["<a>"] = cursor.Tunnel0
    message["<b>"] = cursor.Tunnel1
    message["<c>"] = cursor.grekey

    ff = codecs.open(r'f:\project\vrpcfg1.cfg',"r","gbk")
    output = open(cursor.name.decode("utf8")+".cfg","w")
    p1 = re.compile("<\d>")
    p2 = re.compile("<[abc]>")
    for line in ff:
        for m in p1.finditer(line):
            sub = m.group()
            line = line.replace(sub,message[sub])
        for m in p2.finditer(line):
            sub = m.group()
            line = line.replace(sub,message[sub])
        output.write(line)
    ff.close()
    output.close();
    return None


def getVPN(request):
    rank=request.GET.get("rank")
    rankid=request.GET.get("rankid")
    id=request.GET.get("id")
    cursor=Message.objects.get(id=id)
    createVPN(cursor)
    strr = "VPN文件已生成"
    path = "/getMessage/?id="+id+"&rank="+rank+"&rankid="+rankid
    return render_to_response("hint.html",locals())



#--------------------------------------------------分割线——----------------------------------
#####拼音生成
def convert(ch):
    """
    该函数通过输入汉字返回其拼音，如果输入多个汉字，则返回第一个汉字拼音.
       如果输入数字字符串，或者输入英文字母，则返回其本身(英文字母如果为大写，转化为小写)
    """
    length = len('拼') #测试汉字占用字节数，utf-8，汉字占用3字节.bg2312，汉字占用2字节
    intord = ord(ch[0:1])
    #字母或者数字直接返回
    if (intord >= 48 and intord <= 57):
        return ch[0:1]
    if (intord >= 65 and intord <=90 ) or (intord >= 97 and intord <=122):
        return ch[0:1].lower()
    hanzis=[]
    ch_length = len(ch)
    i = 0
    while True:
        '''
        生成汉字的编码
        '''
        hanzis.append(ch[i:i+length])
        i += length
        if i+length > ch_length:
            break
        pass
    pinyin=[]
    #查询字库获取拼音
    for hanzi in hanzis:
        with open(r'../convert-utf-8.txt') as f:
            for line in f:
                if hanzi in line:
                    pinyin.append( line[length:len(line)-2])
                    pass
                pass
            pass
    return pinyin

#####------------加密开始
from math import sin,cos

def create_x(gong_si_name):
    '''
    根据分支公司名称，创建参数X
    1.获取分支公司名称
    2.根据公司名称生成相应的字符编码值
    3.将获取的编码值求总和sum
    4.求 sin（sum）的值
    5.将sin求得的值与1234567相乘，得到最终的参数x的值
    '''


    if type(gong_si_name).__name__!="unicode":
        gong_si_name=unicode(gong_si_name,"utf8")
    length=len(u"拼")
    ch_length = len(gong_si_name)
    i = 0
    sum = 0
    print gong_si_name[0:1]
    #根据中文字节数划分字符串
    while True:
        chs = gong_si_name[i:i+length]
        #将字符串经过编码后，转为标准的python字符串
        chs = repr(chs.encode("utf8").decode("utf8"))
        #去掉unicode字符串中的"\u"
        chs = str(chs.replace('\\u','')).split("'")[1]
        #将字符串转为数字，求和
        sum += (int(chs,16))
        i += length
        if i+length > ch_length:
            break
    #求sin(sum)的值
    sin_value = sin(sum)
    #生成最终的参数x的值
    x_value = sin_value*1234567
    while len(str(abs(x_value))) < 6:
        x_value += (x_value*1234567)
    return x_value

def create_y(wang_guan):
    '''
    根据内网网关，生成参数Y
    1.获取内网网关的各字段的编码值
    2.求字符编码值的总和sum
    3.求cos（sum）的值
    4.将cos求得的值与7654321相乘，得到最终的参数Y的值
    '''
    sum = 0
    for ch in wang_guan:
        sum += ord(ch)
    cos_value = cos(sum)
    y_value = cos_value*7654321
    while len(str(abs(y_value)))<6:
        y_value += (y_value*7654321)
    return y_value

def create_z(ike_local_name):
    '''
    根据ike-local-name，生成参数z
    1.获取ike-local-name的各字符的编码值
    2.求字符编码值的总和sum
    3.将sum的值与135相乘求得参数z的最终值
    '''
    #去掉字符串中的“-”
    ike_local_name = ike_local_name.replace("-","")
    sum = 0
    for ch in ike_local_name:
        sum += ord(ch)
        pass
    z_value = sum*135790
    while len(str(abs(z_value))) < 6:
        z_value += (z_value*135790)
    return z_value

#生成加密的密码，并返回
def meger(x,y,z):
    '''
    分别将参数x,y,值转换为十六进制数
    参数x取前五位数
    参数y取前五位数
    参数z取前六位数
    合并选取的数获得一个十六位的十六进制数
    '''

    #十进制数转十六进制
    x_hex = hex(int(abs(x)))
    y_hex = hex(int(abs(y)))
    z_hex = hex(int(abs(z)))
    #相应的参数转为字符串
    x_str = str(x_hex)
    y_str = str(y_hex)
    z_str = str(z_hex)
    #去除 十六进制中的 0x
    x_str = x_str.replace("0x","")
    y_str = y_str.replace("0x","")
    z_str = z_str.replace("0x","")
    return x_str[0:6]+y_str[0:6]+z_str[0:6]

def jia_mi(request):
    '''
    x = 分支公司名称
    y = 内网网关
    z = ike_local_name
    '''
    x = ""
    y = ""
    z = ""

    x = create_x(request.POST.get("department"))
    y = create_y(request.POST.get("GATEWAY"))
    z = create_z(request.POST.get("peerID"))

    ike_preshare_key= meger(x,y,z)
    return ike_preshare_key
#--------------------------------------------------------------------------
