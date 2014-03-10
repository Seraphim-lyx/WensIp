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

def setDefaultUser(request):
    """
    初始化账号密码
    """
    User.objects.create(name="admin",password="admin").save()

    return  HttpResponse("ok")

def index(request):
    """
    登陆页面
    """
    if request.session.get('user') is not None:#查询session信息
        return render_to_response("base.html")
    return render_to_response("index.html")

@csrf_exempt
def login(request):
    """
    登陆接口
    """
    name=request.POST.get("username")
    password=request.POST.get("password")
    remenber=request.POST.get("remenber")
    try:
        user=User.objects.get(name=name,password=password)#检验账号密码正确性
        if user is not None:
            if remenber is not None:
                request.session['user']=user.id#设置session记录
            return render_to_response("base.html")
    except:
        return render_to_response("LoginIn.html")

@csrf_exempt
def logout(request):
    """
    安全登出接口
    """
    if request.session.get('user') is not None:
        request.session.clear()#清楚session记录

    return render_to_response("index.html")