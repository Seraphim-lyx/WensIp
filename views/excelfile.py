#coding=utf8
import xlrd
import xlwt
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
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
    #分公司
    messages.append(request.POST.get('name'))
    #机构信息
    messages.append("温氏集团")
    #分支机构名
    messages.append(request.POST.get('department'))
    #线路类型
    messages.append(request.POST.get('circuit'))
    #设备类型
    messages.append(request.POST.get("IAD"))
    #内网段
    diagram = request.POST.get("Diagram")
    messages.append(diagram)
    #内网网关
    gateway=request.POST.get("GATEWAY")
    messages.append(gateway)
    #本地端ID
    messages.append(request.POST.get("peerID"))
    #公网地址
    messages.append(request.POST.get('PublicIP'))
    #所在地DNS
    messages.append(request.POST.get('DNS'))
    #预共享密钥（PSK）
    messages.append('预共享密钥（PSK）?')
    #密码
    messages.append(request.POST.get("currentPassword"))
    #安全提议名称????
    messages.append("安全提议名称\n对等体名称\n安全策略名称?")
    #对端地址?????
    messages.append('对端地址?')
    #identify data 对端ID???????
    messages.append('identify data /对端ID?')
    return messages

def h3c_messages(request):
    '''
    读取网页表格信息
    '''
    messages=[]
    #分公司
    messages.append(request.POST.get('name'))
    #机构
    messages.append("温氏集团")
    #分支机构名
    messages.append(request.POST.get('department'))
    #线路类型
    messages.append(request.POST.get('circuit'))
    #设备类型
    messages.append(request.POST.get("IAD"))
    #内网段
    diagram = request.POST.get("Diagram")
    messages.append(diagram)
    #内网网关
    gateway=request.POST.get("GATEWAY")
    messages.append(gateway)
    #ike-local-name
    messages.append(request.POST.get("peerID"))
    #公网地址
    messages.append(request.POST.get('PublicIP'))
    #所在地DNS
    messages.append(request.POST.get('DNS'))
    #tunnelIP0
    messages.append(request.POST.get("Tunnel0"))
    #tunnelIP1
    messages.append(request.POST.get("Tunnel1"))
    #gre key
    messages.append(request.POST.get("grekey"))
    #ike-pre-share-key
    messages.append(request.POST.get("ikepresharekey"))
    #password
    messages.append(request.POST.get("currentPassword"))
    #1000f ike peer 318的policy name
    messages.append("1000f ike peer/318的policy name")
    return messages

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