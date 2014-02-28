from django.db import models
#coding=utf8


class Message(models.Model):
    id=models.AutoField(primary_key=True)
    #主键
    name=models.CharField(max_length=20)
    #机构名称
    organizeid=models.CharField(max_length=20)
    #机构代号
    operator=models.CharField(max_length=20)
    #所属运营商
    circuit=models.CharField(max_length=20)
    #线路类型
    downlinkBandwidth=models.CharField(max_length=30)
    #下行带宽
    uplinkBandwidth=models.CharField(max_length=30)
    #上行带宽
    PublicIP=models.CharField(max_length=50)
    #公网IP
    PublicGATEWAY=models.CharField(max_length=50)
    #公网网关
    DNS=models.CharField(max_length=50)
    #所在地DNS
    IAD=models.CharField(max_length=40)
    #接入设备类型
    intranetDiagram=models.TextField(max_length=50)
    #内网段
    intranetGATEWAY=models.TextField(max_length=50)
    #内网网关
    networkSupervisor=models.CharField(max_length=50)
    #上网管理设备
    networkSupervisorIP=models.CharField(max_length=50)
    #上网管理设备IP
    deviceDiagram=models.CharField(max_length=30)
    #设备互联网段
    deviceManagement=models.CharField(max_length=30)
    #设备管理信息
    LoopBackIP=models.CharField(max_length=30)
    #LoopBackIP
    deviceService=models.TextField(max_length=30)
    #设备服务
    peerID=models.CharField(max_length=30)
    #IKE local-name/peerID/local identify data
    Tunnel0=models.CharField(max_length=30)
    #Tunnel0
    Tunnel1=models.CharField(max_length=30)
    #Tunnel1

    ##
    #TunnelIP网段
    beginIP = models.CharField(max_length=30)
    endIP = models.CharField(max_length=30)
    ##

    grekey=models.CharField(max_length=30)
    #gre key
    ike_preshare_key=models.CharField(max_length=30)
    #ike_preshare_key
    terminalIkePeer=models.CharField(max_length=30)
    #中心端"ike peer"/终端"policy name"
    centerTunnel=models.CharField(max_length=30)
    #中心端tunnel号
    centerTemplate=models.CharField(max_length=40)
    #中心端ipsec policy-template 模板号
    centerNQA=models.CharField(max_length=30)
    #中心端"NQA" "delete-group"
    username=models.CharField(max_length=30)
    #用户名
    currentPassword=models.CharField(max_length=30)
    #当前密码
    historicalPassword=models.CharField(max_length=30)
    #历史密码
    currentSSH=models.CharField(max_length=30)
    #当前SSH
    historicalSSH=models.CharField(max_length=30)
    #历史SSH
    nat=models.TextField(max_length=300)
    #nat情况
    note=models.TextField(max_length=300)
    #备注
    rank=models.CharField(max_length=50)
    #机构层级

#二级机构
class SecRank(models.Model):
    id=models.AutoField(primary_key=True)
    organizeid=models.CharField(max_length=20)
    name=models.CharField(max_length=20)
    message=models.OneToOneField(Message,null=True)


#二级半机构
class SecHalfRank(models.Model):
    id=models.AutoField(primary_key=True)
    organizeid=models.CharField(max_length=20)
    name=models.CharField(max_length=20)
    message=models.OneToOneField(Message,null=True)
    parent_rank=models.ForeignKey(SecRank,null=True)

#三级机构
class ThiRank(models.Model):
    id=models.AutoField(primary_key=True)
    organizeid=models.CharField(max_length=20)
    name=models.CharField(max_length=20)
    message=models.OneToOneField(Message,null=True)
    parent_rank=models.ForeignKey(SecRank,null=True)
    parent_rank_half=models.ForeignKey(SecHalfRank,null=True)

#四级机构
class FouRank(models.Model):
    id=models.AutoField(primary_key=True)
    organizeid=models.CharField(max_length=20)
    name=models.CharField(max_length=20)
    message=models.OneToOneField(Message,null=True)
    parent_rank=models.ForeignKey(ThiRank,null=True)

#抽象化选项
class Abstraction(models.Model):
    id=models.AutoField(primary_key=True)
    type=models.IntegerField(null=True)
    #选项类型
    name=models.CharField(max_length=50)
    #选项名称

class atest(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=30)

class tt(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=20)
    tess=models.ForeignKey(atest,null=True)

class cc(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=20)
    tess=models.ForeignKey(atest,null=True)

#用户列表
class User(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=30)
    password=models.CharField(max_length=30)

#
class ExtraField(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)

class File(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    uuid=models.CharField(max_length=50)
    content=models.CharField(max_length=250)
    date=models.DateField(null=True)
    file=models.ForeignKey(Message,null=True)