#coding=utf-8
from django import forms
from mis.models import File
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from datetime import *

import uuid
import time

class UploadFileForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput, required=False)

def SaveFile(request,mes):
    """
    上传文件
    """
    try:
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file=request.FILES['file']
            dir="static"
            name=file.name
            str=name.split(".")[1]
            filename=uuid.uuid4().__str__()

            with open(dir+'/'+filename+'.'+str,'wb+') as path:
                for chunk in file.chunks():
                    path.write(chunk)

            f=File.objects.create()
            f.name=name
            f.uuid=filename
            f.date=datetime.today()
            f.file=mes
            f.save()
    except:
        return None


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

