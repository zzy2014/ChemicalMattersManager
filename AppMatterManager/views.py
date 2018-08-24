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
    elif (strPageType == "showMatterStates"):
        return render_to_response("showJsGrid.html", context)
    elif (strPageType == "showMatterTypes"):
        return render_to_response("showJsGrid.html", context)
    elif (strPageType == "showMatterUnits"):
        return render_to_response("showJsGrid.html", context)
    elif (strPageType == "showPurityLevels"):
        return render_to_response("showJsGrid.html", context)
    elif (strPageType == "showStoreRooms"):
        return render_to_response("showJsGrid.html", context)
    else:
        return HttpResponse("")


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


#药品理化状态
class CMatterStatesView(Resource):

    def get(self, request):
        strId = request.GET.get("id", "") 
        strStateName = request.GET.get("EF_StateName", "") 
        arrValidStates = MatterStates.objects.all() 

        if (strId != ""):
            arrValidStates = arrValidStates.filter(id__contains = int(strId))
        if (strStateName != ""):
            arrValidStates = arrValidStates.filter(EF_StateName__contains = strStateName)

        return HttpResponse(self.to_json(arrValidStates), content_type = 'application/json', status = 200)

    def post(self, request):
        strStateName = request.POST.get("EF_StateName", "")
        newItem = MatterStates.objects.create(EF_StateName = strStateName)
        return JsonResponse({"id":newItem.id,"EF_StateName":newItem.EF_StateName}, status = 201)

    def put(self, request):
        intCurId = int(request.PUT.get("id"))
        curState = MatterStates.objects.get(id = intCurId)
        curState.EF_StateName = request.PUT.get("EF_StateName", "")
        curState.save()
        return JsonResponse({"id":curState.id, "EF_StateName":curState.EF_StateName}, status = 200)

    def delete(self, request, intTypeId):
        curState = MatterStates.objects.get(id = int(intTypeId))
        curState.delete()
        return HttpResponse(status = 200)

    def to_json(self, objects):
        return serializers.serialize('json', objects)


#纯度规格
class CPurityLevelsView(Resource):

    def get(self, request):
        strId = request.GET.get("id", "") 
        strLevelName = request.GET.get("EF_LevelName", "") 
        arrValidLevels = PurityLevels.objects.all() 

        if (strId != ""):
            arrValidLevels = arrValidLevels.filter(id__contains = int(strId))
        if (strLevelName != ""):
            arrValidLevels = arrValidLevels.filter(EF_LevelName__contains = strLevelName)

        return HttpResponse(self.to_json(arrValidLevels), content_type = 'application/json', status = 200)

    def post(self, request):
        strLevelName = request.POST.get("EF_LevelName", "")
        newItem = PurityLevels.objects.create(EF_LevelName = strLevelName)
        return JsonResponse({"id":newItem.id,"EF_LevelName":newItem.EF_LevelName}, status = 201)

    def put(self, request):
        intCurId = int(request.PUT.get("id"))
        curLevel = PurityLevels.objects.get(id = intCurId)
        curLevel.EF_LevelName = request.PUT.get("EF_LevelName", "")
        curLevel.save()
        return JsonResponse({"id":curLevel.id, "EF_LevelName":curLevel.EF_LevelName}, status = 200)

    def delete(self, request, intTypeId):
        curLevel = PurityLevels.objects.get(id = int(intTypeId))
        curLevel.delete()
        return HttpResponse(status = 200)

    def to_json(self, objects):
        return serializers.serialize('json', objects)


#药品类别
class CMatterTypesView(Resource):

    def get(self, request):
        strId = request.GET.get("id", "") 
        strName = request.GET.get("EF_TypeName", "") 
        arrValidItems = MatterTypes.objects.all() 

        if (strId != ""):
            arrValidItems = arrValidItems.filter(id__contains = int(strId))
        if (strName != ""):
            arrValidItems = arrValidItems.filter(EF_TypeName__contains = strName)

        return HttpResponse(self.to_json(arrValidItems), content_type = 'application/json', status = 200)

    def post(self, request):
        strName = request.POST.get("EF_TypeName", "")
        newItem = MatterTypes.objects.create(EF_TypeName = strName)
        return JsonResponse({"id":newItem.id,"EF_TypeName":newItem.EF_TypeName}, status = 201)

    def put(self, request):
        intCurId = int(request.PUT.get("id"))
        curItem = MatterTypes.objects.get(id = intCurId)
        curItem.EF_TypeName = request.PUT.get("EF_TypeName", "")
        curItem.save()
        return JsonResponse({"id":curItem.id, "EF_TypeName":curItem.EF_TypeName}, status = 200)

    def delete(self, request, intTypeId):
        curItem = MatterTypes.objects.get(id = int(intTypeId))
        curItem.delete()
        return HttpResponse(status = 200)

    def to_json(self, objects):
        return serializers.serialize('json', objects)


#药品仓库
class CStoreRoomsView(Resource):

    def get(self, request):
        strId = request.GET.get("id", "") 
        strName = request.GET.get("EF_RoomName", "") 
        arrValidItems = StoreRooms.objects.all() 

        if (strId != ""):
            arrValidItems = arrValidItems.filter(id__contains = int(strId))
        if (strName != ""):
            arrValidItems = arrValidItems.filter(EF_RoomName__contains = strName)

        return HttpResponse(self.to_json(arrValidItems), content_type = 'application/json', status = 200)

    def post(self, request):
        strName = request.POST.get("EF_RoomName", "")
        newItem = StoreRooms.objects.create(EF_RoomName = strName)
        return JsonResponse({"id":newItem.id,"EF_RoomName":newItem.EF_RoomName}, status = 201)

    def put(self, request):
        intCurId = int(request.PUT.get("id"))
        curItem = StoreRooms.objects.get(id = intCurId)
        curItem.EF_RoomName = request.PUT.get("EF_RoomName", "")
        curItem.save()
        return JsonResponse({"id":curItem.id, "EF_RoomName":curItem.EF_RoomName}, status = 200)

    def delete(self, request, intTypeId):
        curItem = StoreRooms.objects.get(id = int(intTypeId))
        curItem.delete()
        return HttpResponse(status = 200)

    def to_json(self, objects):
        return serializers.serialize('json', objects)

