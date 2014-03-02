#coding=utf-8
from django import forms
from mis.models import File
from mis.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from datetime import *

import uuid
import os

class UploadFileForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput, required=False)

@csrf_exempt
def SaveFile(request,mes):
    """
    上传文件
    """
    try:
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file=request.FILES['file']
            dir="static/files"
            name=file.name
            str=name.split(".")[1]
            uid=uuid.uuid4().__str__()

            with open(dir+'/'+uid+'.'+str,'wb+') as path:
                for chunk in file.chunks():
                    path.write(chunk)
            filename=request.POST.get("filename")
            content=request.POST.get("content")
            f=File.objects.create()
            f.name=filename
            f.uuid=uid+"."+str
            f.date=datetime.today()
            f.file=mes
            f.content=content
            f.save()
    except:
        return None


@csrf_exempt
def ReadFile(request):
    """
    下载文件
    """
    id=request.GET.get("id")
    f=File.objects.get(id=id)
    uid=f.uuid
    file_name = "static/files/"+uid
    c=open(file_name,"rb").read()
    response = HttpResponse(c,mimetype='text/plain')
    response['Content-Disposition'] = 'attachment; filename='+f.name
    return response

@csrf_exempt
def DeleteFile(request):
    """
    删除数据库内容
    删除文件实体
    """
    id=request.POST.get("id")
    organid=request.POST.get("organid")
    f=File.objects.get(id=id)
    if f is not None:
        uid=f.uuid
        path="static/files/"+uid
        print path
        os.remove(path)
        f.delete()
    files=Message.objects.get(id=organid).file_set.all()
    return render_to_response("message/FileList.html",locals())

@csrf_exempt
def GetFileList(request):
    id=request.POST.get("id")
    files=Message.objects.get(id=id).file_set.all()
    return render_to_response("message/FileList.html",locals())