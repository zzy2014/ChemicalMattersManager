# coding=utf8
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render, render_to_response
from simple_rest import Resource #第三方的小类
from django.core import serializers #导入序列化
from django.core.files.base import ContentFile
import json
from AppUserManager.views import getCurUser
from AppMatterSetting.models import MatterUnits, MatterStates
from AppMatterSetting.models import PurityLevels, MatterTypes, StoreRooms, Matters
from AppMatterSetting.models import MatterAlerts, MatterMinRemains, MatterAccessBlocks, SubMatterAccessBlocks
from .models import CensorePatterns, CensoreStates, FormStates, ImportForms, MatterDetails

#获取userHome界面中的右侧界面
def showOneTable(request):
    userDict = getCurUser(request)
    curUser = userDict["curUser"]
    if (curUser == ""):
        return HttpResponse("用户尚未登录！")

    if (request.method != "POST"):
        return HttpResponse("访问类型错误！")

    strPageType = request.POST.get('pageType')
    if (strPageType == ""):
        return HttpResponse("页面类型无效！")

    context = {} #一个字典对象
    context["pageType"] = strPageType

    if (strPageType == "showCensoreStates"):
        return render_to_response("showOneTable.html", context)
    elif (strPageType == "showCensorePatters"):
        return render_to_response("showOneTable.html", context)
    elif (strPageType == "showImportForm"):
        return render_to_response("showOneTable.html", context)
    else:
        return HttpResponse("")


#获取userHome界面中的右侧界面--上下表格
def showTwoTables(request):
    userDict = getCurUser(request)
    curUser = userDict["curUser"]
    if (curUser == ""):
        return HttpResponse("用户尚未登录！")

    if (request.method != "POST"):
        return HttpResponse("访问类型错误！")

    strPageType = request.POST.get('pageType')
    if (strPageType == ""):
        return HttpResponse("页面类型无效！")

    context = {} #一个字典对象
    context["pageType"] = strPageType

    if (strPageType == "showMatterAccessBlocks"):
        return render_to_response("showTwoTables.html", context)
    else:
        return HttpResponse("")


#审核状态
class CCensoreStatesView(Resource):

    def get(self, request):
        strId = request.GET.get("id", "") 
        strName = request.GET.get("EF_States", "") 
        arrValidItems = CensoreStates.objects.all() 

        if (strId != ""):
            arrValidItems = arrValidItems.filter(id__contains = int(strId))
        if (strName != ""):
            arrValidItems = arrValidItems.filter(EF_States__contains = strName)

        return HttpResponse(self.to_json(arrValidItems), content_type = 'application/json', status = 200)

    def post(self, request):
        strName = request.POST.get("EF_States", "")
        newItem = CensoreStates.objects.create(EF_States = strName)
        return JsonResponse({"id":newItem.id,"EF_States":newItem.EF_States}, status = 201)

    def put(self, request):
        intCurId = int(request.PUT.get("id"))
        curItem = CensoreStates.objects.get(id = intCurId)
        curItem.EF_States= request.PUT.get("EF_States", "")
        curItem.save()
        return JsonResponse({"id":curItem.id, "EF_States":curItem.EF_States}, status = 200)

    def delete(self, request, intTypeId):
        curItem = CensoreStates.objects.get(id = int(intTypeId))
        curItem.delete()
        return HttpResponse(status = 200)

    def to_json(self, objects):
        return serializers.serialize('json', objects)


#审核流程
class CCensorePatternsView(Resource):

    def get(self, request):
        strId = request.GET.get("id", "") 
        strStepsCount = request.GET.get("EF_StepsCount", "0") 
        strUserTypeId1 = request.GET.get("EF_UserTypeId1", "0") 
        strUserTypeId2 = request.GET.get("EF_UserTypeId2", "0") 
        strUserTypeId3 = request.GET.get("EF_UserTypeId3", "0") 
        arrValidItems = CensorePatterns.objects.all() 

        if (strId != ""):
            arrValidItems = arrValidItems.filter(id__contains = int(strId))
        if (strStepsCount != ""):
            arrValidItems = arrValidItems.filter(EF_StepsCount__contains = strStepsCount)
        if (strUserTypeId1 != ""):
            arrValidItems = arrValidItems.filter(EF_UserTypeId1__contains = strUserTypeId1)
        if (strUserTypeId2 != ""):
            arrValidItems = arrValidItems.filter(EF_UserTypeId2__contains = strUserTypeId2)
        if (strUserTypeId3 != ""):
            arrValidItems = arrValidItems.filter(EF_UserTypeId3__contains = strUserTypeId3)

        return HttpResponse(self.to_json(arrValidItems), content_type = 'application/json', status = 200)

    def post(self, request):
        strStepsCount = request.POST.get("EF_StepsCount", "0") 
        strUserTypeId1 = request.POST.get("EF_UserTypeId1", "0") 
        strUserTypeId2 = request.POST.get("EF_UserTypeId2", "0") 
        strUserTypeId3 = request.POST.get("EF_UserTypeId3", "0") 
        newItem = CensorePatterns.objects.create(EF_StepsCount = strStepsCount, EF_UserTypeId1 = strUserTypeId1,
                EF_UserTypeId2 = strUserTypeId2, EF_UserTypeId3 = strUserTypeId3)

        jsonDict = {}
        jsonDict["id"] = newItem.id
        jsonDict["EF_StepsCount"] = int(strStepsCount)
        jsonDict["EF_UserTypeId1"] = int(strUserTypeId1)
        jsonDict["EF_UserTypeId2"] = int(strUserTypeId2)
        jsonDict["EF_UserTypeId3"] = int(strUserTypeId3)
        jsonStr = json.dumps(jsonDict, ensure_ascii=True) 

        return JsonResponse(jsonStr, status = 201, safe=False)

    def put(self, request):
        strStepsCount = request.PUT.get("EF_StepsCount", "0") 
        strUserTypeId1 = request.PUT.get("EF_UserTypeId1", "0") 
        strUserTypeId2 = request.PUT.get("EF_UserTypeId2", "0") 
        strUserTypeId3 = request.PUT.get("EF_UserTypeId3", "0") 
        curItem = CensorePatterns.objects.get(id = intCurId)
        curItem.EF_StepsCount = int(strStepsCount)
        curItem.EF_UserTypeId1 = int(strUserTypeId1)
        curItem.EF_UserTypeId2 = int(strUserTypeId2)
        curItem.EF_UserTypeId3 = int(strUserTypeId3)
        curItem.save()

        jsonDict = {}
        jsonDict["id"] = newItem.id
        jsonDict["EF_StepsCount"] = int(strStepsCount)
        jsonDict["EF_UserTypeId1"] = int(strUserTypeId1)
        jsonDict["EF_UserTypeId2"] = int(strUserTypeId2)
        jsonDict["EF_UserTypeId3"] = int(strUserTypeId3)
        jsonStr = json.dumps(jsonDict, ensure_ascii=True) 

        return JsonResponse(jsonStr, status = 200, safe=False)

    def delete(self, request, intTypeId):
        curItem = CensorePatterns.objects.get(id = int(intTypeId))
        curItem.delete()
        return HttpResponse(status = 200)

    def to_json(self, objects):
        return serializers.serialize('json', objects)

