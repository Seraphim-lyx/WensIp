#coding=utf8
import xlrd
import xlwt
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from message_dao import GetRank,convert

from mis import models
def excel_init(select_index):
    '''
    重相应的excel文件中获取excel文件的表头信息
    '''
    header=[]
    r_file = xlrd.open_workbook('excel_template.xls',encoding_override='utf8')
    sheet = r_file.sheet_by_index(0)
    for index in range(15+select_index):
        try:
            header.append(sheet.cell(select_index,index).value)
        except :
            header.append("")
            pass
    return header

def junniper_messages(request):
    '''
    读取网页表格信息
    '''
    messages=[]
    rank=request.GET.get("rank")
    rankid=request.GET.get("rankid")
    id=request.GET.get("id")
    data = models.Message.objects.get(id=id)
    obj=GetRank(rank).get(id=rankid)

    def setName(*names):
        for name in names:
            messages.append(name)
        return None

    # 设置 分公司 机构 分支机构名称
    if rank == '2':
        setName(obj.name,obj.name,obj.name)
    elif rank == '2.5':
        setName(obj.parent_rank.name,obj.parent_rank.name,obj.name)
    elif rank == "3":
        if obj.parent_rank is not None:
            setName(obj.parent_rank.name,obj.parent_rank.name,obj.name)
        else:
            setName(obj.parent_rank_half.parent_rank.name,obj.parent_rank_half.name,obj.name)
    elif rank == '4':
        if obj.parent_rank.parent_rank is not None:
            setName(obj.parent_rank.parent_rank.name,obj.parent_rank.name,obj.name)
        else:
            setName(obj.parent_rank.parent_rank_half.name,obj.parent_rank.name,obj.name)
    #线路类型
    messages.append(data.circuit)
    #设备类型
    messages.append(data.IAD)
    #内网段
    messages.append(data.intranetDiagram)
    #内网网关
    messages.append(data.intranetGATEWAY)
    #本地端ID
    first = " ".join(convert(messages[0])).title().replace(" ","")
    second = " " .join(convert(messages[1])).title().replace(" ","")
    third = " ".join(convert(messages[2])).title().replace(" ","")
    local_id = first+"-"+second+"-"+third
    messages.append(local_id)
    #公网地址
    messages.append(data.PublicIP)
    #所在地DNS
    messages.append(data.DNS)
    #预共享密钥（PSK）
    messages.append(data.PSK)
    #密码
    messages.append(data.currentPassword)
    #安全提议名称????
    first = get_short_cut(convert(messages[0]))
    second = get_short_cut(convert(messages[1]))
    third = data.grekey
    messages.append(first+"-"+second+"-"+third)
    #对端地址?????
    messages.append('219.131.174.199')
    #identify data 对端ID???????
    messages.append('XXZX-SSG520')
    return messages

def h3c_messages(request):
    '''
    读取网页表格信息
    '''
    messages=[]
    rank=request.GET.get("rank")
    rankid=request.GET.get("rankid")
    id=request.GET.get("id")
    data = models.Message.objects.get(id=id)
    obj=GetRank(rank).get(id=rankid)

    def setName(*names):
        for name in names:
            messages.append(name)
        return None
    if rank == '2':
        setName(obj.name,obj.name,obj.name)
    elif rank == '2.5':
        setName(obj.parent_rank.name,obj.parent_rank.name,obj.name)
    elif rank == "3":
        if obj.parent_rank is not None:
            setName(obj.parent_rank.name,obj.parent_rank.name,obj.name)
        else:
            setName(obj.parent_rank_half.parent_rank.name,obj.parent_rank_half.name,obj.name)
    elif rank == '4':
        if obj.parent_rank.parent_rank is not None:
            setName(obj.parent_rank.parent_rank.name,obj.parent_rank.name,obj.name)
        else:
            setName(obj.parent_rank.parent_rank_half.name,obj.parent_rank.name,obj.name)
    #线路类型
    messages.append(data.circuit)
    #设备类型
    messages.append(data.IAD)
    #内网段
    messages.append(data.intranetDiagram)
    #内网网关
    messages.append(data.intranetGATEWAY)
    #ike-local-name
    messages.append(data.peerID)
    #公网地址
    messages.append(data.PublicIP)
    #所在地DNS
    messages.append(data.DNS)
    #tunnelIP0
    messages.append(data.Tunnel0)
    #tunnelIP1
    messages.append(data.Tunnel1)
    #gre key
    messages.append(data.grekey)
    #ike-pre-share-key
    messages.append(data.ike_preshare_key)
    #password
    messages.append(data.currentPassword)
    #1000f ike peer 318的policy name
    #
    # 分公司（拼音）-机构（拼音）-grekey
    first = ""
    second = ""
    third = data.grekey
    policy_name = ""
    first = get_short_cut(convert(messages[0]))
    second = get_short_cut(convert(messages[1]))
    try:
        policy_name = first+"-"+second+"-"+str(third)
    except:
        policy_name = first+"-"+second+"-"+"???"
    messages.append(policy_name)
    return messages


def get_short_cut(pinyin):
    short = ""
    for letter in pinyin:
        short += letter[0]
    return short
def write_excel(excelCaption,messages,filename):
    '''
    初始化准备写的excel文件
    并设置excel文件的单元格大小，颜色的style
    '''
    w_file = xlwt.Workbook(encoding='utf8')
    sheet = w_file.add_sheet('配置表',cell_overwrite_ok=True)
    style =  xlwt.easyxf('pattern:pattern alt_bars, fore_colour tan,back_color tan;'
                        'align:vertical center, horizontal center,wrap on;'
                        'borders:left 1,right 1,top 1,bottom 1;'
                        'font: bold off,colour_index black,height 200;')
    for index,head in enumerate(excelCaption):
        sheet.write(0,index,head,style)
        sheet.col(index).width = 4000+len(head)*100

    style =  xlwt.easyxf(#'pattern:pattern solid;'
                        'align: vertical center, horizontal center,wrap on;'
                        'borders:left 1,right 1,top 1,bottom 1;'
                        )
    for index,message in enumerate(messages):
        try:
            sheet.write(1,index,message,style)
        except:
            pass
    try:
        w_file.save(filename)
    except IOError:
        pass
    return None
    pass
def excel_request(request):
    '''
    处理来自网页的excel需求
    '''

    try:
        filetype = int(request.GET.get("filetype"))
    except TypeError:
        return HttpResponse("Excel Error")
        pass
    excelCaption=excel_init(filetype)
    messages = None
    if filetype is None:
        return HttpResponse("No Message can Write")
    elif filetype == 0:
        messages = junniper_messages(request)
        geshi = "_Junniper.xls"
    elif filetype == 1:
        messages = h3c_messages(request)
        geshi = "_H3C.xls"

    filename = ""
    id = request.GET.get("id")
    try:
        filename = models.Message.objects.get(id=id).name.decode("utf8")+".xls"

    except :
        filename = u"未知.xls"
        pass
    write_excel(excelCaption,messages,filename)

    return ReadFile(request,filename,geshi)

from django.core.servers.basehttp import FileWrapper
import os

def ReadFile(request,filename,geshi):
    """
    下载文件
    """
         # Select your file here.
    import StringIO
    f = open(filename,"rb")
    output = StringIO.StringIO()
    output.write(f.read())
    f.close()
    wrapper = FileWrapper(file(filename))
    response = HttpResponse(content=output.getvalue(),mimetype='application/vnd.ms-excel')

    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Disposition'] = 'attachment; filename = %s' % filename.encode("utf8").replace(".xls",geshi)
    return response





def test(request):
    return render_to_response("test3.html")