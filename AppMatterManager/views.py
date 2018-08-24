# coding=utf8
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render, render_to_response
from simple_rest import Resource #第三方的小类
from django.core import serializers #导入序列化
from django.core.files.base import ContentFile
from AppUserManager.views import getCurUser
from .models import MatterUnits, MatterStates
from .models import PurityLevels, MatterTypes, StoreRooms, Matters
from .models import MatterAlerts, MatterMinRemains, MatterAccessBlocks
import json

#获取userHome界面中的右侧界面
def showRightPage(request):
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

    if (strPageType == "showMatterUnits"):
        return render_to_response("showJsGrid.html", context)


#药品单位接口
class CMatterUnitsView(Resource):

    def get(self, request):
        strId = request.GET.get("id", "") 
        strUnitName = request.GET.get("EF_UnitName", "") 
        arrValidUnits = MatterUnits.objects.all() 

        if (strId != ""):
            arrValidUnits = arrValidUnits.filter(id__contains = int(strId))
        if (strUnitName != ""):
            arrValidUnits = arrValidUnits.filter(EF_UnitName__contains = strUnitName)

        return HttpResponse(self.to_json(arrValidUnits), content_type = 'application/json', status = 200)

    def post(self, request):
        strUnitName = request.POST.get("EF_UnitName", "")
        newItem = MatterUnits.objects.create(EF_UnitName = strUnitName)
        return JsonResponse({"id":newItem.id,"EF_UnitName":newItem.EF_UnitName}, status = 201)

    def put(self, request):
        intCurId = int(request.PUT.get("id"))
        curUnit = MatterUnits.objects.get(id = intCurId)
        curUnit.EF_UnitName= request.PUT.get("EF_UnitName", "")
        curUnit.save()
        return JsonResponse({"id":curUnit.id, "EF_UnitName":curUnit.EF_UnitName}, status = 200)

    def delete(self, request, intTypeId):
        curUnit = MatterUnits.objects.get(id = int(intTypeId))
        curUnit.delete()
        return HttpResponse(status = 200)

    def to_json(self, objects):
        return serializers.serialize('json', objects)

