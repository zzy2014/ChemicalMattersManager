from django.http import HttpResponse,JsonResponse
from django.shortcuts import render, render_to_response
from simple_rest import Resource #第三方的小类
from django.core import serializers #导入序列化
from django.core.files.base import ContentFile
import json
import sys
from AppUserManager.views import getCurUser
from AppUserManager.models import Teachers
from .models import Finances


#获取userHome界面中的右侧界面
def showOneTable(request):
    userDict = getCurUser(request)
    curUser = userDict["curUser"]
    if (curUser == ""):
        return HttpResponse("用户尚未登录！", status = 403)

    if (request.method != "POST"):
        return HttpResponse("访问类型错误！", status = 403)

    strPageType = request.POST.get('pageType')
    if (strPageType == ""):
        return HttpResponse("页面类型无效！", status = 403)

    context = {} #一个字典对象
    context["pageType"] = strPageType

    if (strPageType == ""):
        return HttpResponse("")
    else:
        return render_to_response("showOneTable.html", context)


#获取userHome界面中的右侧界面--上下表格
def showTwoTables(request):
    userDict = getCurUser(request)
    curUser = userDict["curUser"]
    if (curUser == ""):
        return HttpResponse("用户尚未登录！", status = 403)

    if (request.method != "POST"):
        return HttpResponse("访问类型错误！", status = 403)

    strPageType = request.POST.get('pageType')
    if (strPageType == ""):
        return HttpResponse("页面类型无效！", status = 403)

    context = {} #一个字典对象
    context["pageType"] = strPageType

    if (strPageType == ""):
        return HttpResponse("")
    else:
        return render_to_response("showTwoTables.html", context)


#经费接口
class CFinancesView(Resource):

    def get(self, request):
        strId = request.GET.get("id", "") 
        strName = request.GET.get("EF_Name", "") 
        strAmount = request.GET.get("EF_TotalAmount", "") 
        strTeacherId = request.GET.get("EF_TeacherId", "") 
        arrAllItems = Finances.objects.all()
        arrValidItems = arrAllItems

        if (strId != ""):
            arrValidItems = arrValidItems.filter(id__contains = int(strId))
        if (strName != ""):
            arrValidItems = arrValidItems.filter(EF_Name__contains = strName)
        if (strAmount != ""):
            arrValidItems = arrValidItems.filter(EF_TotalAmount__contains = float(strAmount))
        if (strTeacherId != "" and strTeacherId != "0"):
            arrValidItems = arrValidItems.filter(EF_TeacherId__contains = int(strTeacherId))

        return HttpResponse(self.to_json(arrValidItems), content_type = 'application/json', status = 200)

    def post(self, request):
        strName = request.POST.get("EF_Name", "") 
        strAmount = request.POST.get("EF_TotalAmount", "") 
        if (strAmount == ""):
            strAmount = "0.0"
        strTeacherId = request.POST.get("EF_TeacherId", "") 
        print(strAmount)
        newItem = Finances.objects.create(EF_Name = strName, EF_TotalAmount = float(strAmount), EF_TeacherId = int(strTeacherId))

        jsonDict = {}
        jsonDict["id"] = newItem.id
        jsonDict["EF_Name"] = strName
        jsonDict["EF_TotalAmount"] = strAmount
        jsonDict["EF_TeacherId"] = int(strTeacherId)

        jsonStr = json.dumps(jsonDict, ensure_ascii=False) 

        return JsonResponse(jsonStr, status = 201, safe=False)

    def put(self, request):
        intCurId = int(request.PUT.get("id"))
        strName = request.PUT.get("EF_Name", "") 
        strAmount = request.PUT.get("EF_TotalAmount", "") 
        if (strAmount == ""):
            strAmount = "0.0"
        strTeacherId = request.PUT.get("EF_TeacherId", "0") 

        curAdmin = Finances.objects.get(id = intCurId)
        curAdmin.EF_Name = strName
        curAdmin.EF_TotalAmount = float(strAmount)
        curAdmin.EF_TeacherId = int(strTeacherId)
        curAdmin.save()

        jsonDict = {}
        jsonDict["id"] = intCurId 
        jsonDict["EF_Name"] = strName
        jsonDict["EF_TotalAmount"] = strAmount
        jsonDict["EF_TeacherId"] = strTeacherId

        jsonStr = json.dumps(jsonDict, ensure_ascii=False) 

        return JsonResponse(jsonStr, status = 200, safe = False)

    def delete(self, request, intTypeId):
        curAdmin = Finances.objects.get(id = int(intTypeId))
        curAdmin.delete()
        return HttpResponse(status = 200)

    def to_json(self, objects):
        return serializers.serialize('json', objects)


