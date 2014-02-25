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


def GetOptionList(request):
    type=request.GET.get("type")
    if type is None:
        type=-1
    abs=Abstraction.objects.filter(type=type)
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