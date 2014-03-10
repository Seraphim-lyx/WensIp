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


from project import settings
from mis.models import *


def GetOptionList(request):
    type=request.GET.get("type")
    if type is None:
        type=-1
    abs=Abstraction.objects.filter(type=type)
    typename=""
    if type == "1":
        typename="所属运营商"
    elif type == "2":
        typename="线路类型"
    elif type == "3":
        typename="设备厂商"
    elif type == "4":
        typename="下行带宽"
    elif type == "5":
        typename="上行带宽"
    print typename
    return render_to_response("option/OptionIndex.html",locals())

@csrf_exempt
def AddOption(request):
    type=request.POST.get("type")
    name=request.POST.get("name")
    abs=Abstraction.objects.create(name=name,type=int(type)).save()

    return HttpResponseRedirect("/GetOptionList/?type="+type)

def DelOption(request):
    id=request.GET.get("id")
    abs=Abstraction.objects.get(id=id)
    type=abs.type
    abs.delete()
    strr="删除成功！"
    path="/GetOptionList/?type="+str(type)
    return render_to_response("hint.html",locals())