# coding=utf8
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render, render_to_response
from simple_rest import Resource #第三方的小类
from django.core import serializers #导入序列化
from django.core.files.base import ContentFile
from AppUserManager.views import getCurUser
from .models import MatterUnits, MatterStates
from .models import PurityLevels, MatterTypes, StoreRooms, Matters
from .models import MatterAlerts, MatterMinRemains, MatterAccessBlocks, SubMatterAccessBlocks
import json

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

    if (strPageType == "showMatterUnits"):
        return render_to_response("showOneTable.html", context)
    elif (strPageType == "showMatterStates"):
        return render_to_response("showOneTable.html", context)
    elif (strPageType == "showMatterTypes"):
        return render_to_response("showOneTable.html", context)
    elif (strPageType == "showMatterUnits"):
        return render_to_response("showOneTable.html", context)
    elif (strPageType == "showPurityLevels"):
        return render_to_response("showOneTable.html", context)
    elif (strPageType == "showStoreRooms"):
        return render_to_response("showOneTable.html", context)
    elif (strPageType == "showMatters"):
        return render_to_response("showOneTable.html", context)
    elif (strPageType == "showMatterAlerts"):
        return render_to_response("showOneTable.html", context)
    elif (strPageType == "showMatterMinRemains"):
        return render_to_response("showOneTable.html", context)
    elif (strPageType == "showMatterAccessBlocks"):
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


#所有药品
class CMattersView(Resource):

    def get(self, request):
        strId = request.GET.get("id", "") 
        strTypeId = request.GET.get("EF_TypeId", "") 
        strStateId = request.GET.get("EF_StateId", "") 
        strPurityId = request.GET.get("EF_PurityId", "") 
        strUnitId = request.GET.get("EF_UnitId", "") 
        strStoreId = request.GET.get("EF_StoreId", "") 
        strName = request.GET.get("EF_Name", "") 
        strCas = request.GET.get("EF_CAS", "") 
        strFormat = request.GET.get("EF_Format", "") 
        strAmount = request.GET.get("EF_Amount", "") 
        strPrice = request.GET.get("EF_Price", "") 
        strLocation = request.GET.get("EF_Location", "") 
        strSaler = request.GET.get("EF_Saler", "") 
        strNote = request.GET.get("EF_Note", "") 
        arrValidItems = Matters.objects.all() 

        if (strId != ""):
            arrValidItems = arrValidItems.filter(id__contains = int(strId))
        if (strTypeId != "" and strTypeId != "0"):
            arrValidItems = arrValidItems.filter(EF_TypeId__contains = strTypeId)
        if (strStateId != "" and strStateId != "0"):
            arrValidItems = arrValidItems.filter(EF_StateId__contains = strStateId)
        if (strPurityId != "" and strPurityId != "0"):
            arrValidItems = arrValidItems.filter(EF_PurityId__contains = strPurityId)
        if (strUnitId != "" and strUnitId != "0"):
            arrValidItems = arrValidItems.filter(EF_UnitId__contains = strUnitId)
        if (strStoreId != "" and strUnitId != "0"):
            arrValidItems = arrValidItems.filter(EF_StoreId__contains = strStoreId)
        if (strName != ""):
            arrValidItems = arrValidItems.filter(EF_Name__contains = strName)
        if (strCas != ""):
            arrValidItems = arrValidItems.filter(EF_CAS__contains = strCas)
        if (strFormat != ""):
            arrValidItems = arrValidItems.filter(EF_Format__contains = strFormat)
        if (strAmount != ""):
            arrValidItems = arrValidItems.filter(EF_Amount__contains = strAmount)
        if (strPrice != ""):
            arrValidItems = arrValidItems.filter(EF_Price__contains = strPrice)
        if (strLocation != ""):
            arrValidItems = arrValidItems.filter(EF_Location__contains = strLocation)
        if (strSaler != ""):
            arrValidItems = arrValidItems.filter(EF_Saler__contains = strSaler)
        if (strNote != ""):
            arrValidItems = arrValidItems.filter(EF_Note__contains = strNote)


        return HttpResponse(self.to_json(arrValidItems), content_type = 'application/json', status = 200)

    def post(self, request):
        strTypeId = request.POST.get("EF_TypeId", "") 
        strStateId = request.POST.get("EF_StateId", "") 
        strPurityId = request.POST.get("EF_PurityId", "") 
        strUnitId = request.POST.get("EF_UnitId", "") 
        strStoreId = request.POST.get("EF_StoreId", "") 
        strName = request.POST.get("EF_Name", "") 
        strCas = request.POST.get("EF_CAS", "") 
        strFormat = request.POST.get("EF_Format", "") 
        strAmount = request.POST.get("EF_Amount", "") 
        if (strAmount == ""):
            strAmount = "0"
        strPrice = request.POST.get("EF_Price", "") 
        if (strPrice == ""):
            strPrice = "0.0"
        strLocation = request.POST.get("EF_Location", "") 
        strSaler = request.POST.get("EF_Saler", "") 
        strNote = request.POST.get("EF_Note", "") 
        newItem = Matters.objects.create(EF_TypeId = strTypeId, EF_StateId = strStateId, EF_PurityId = strPurityId,
                EF_UnitId = strUnitId, EF_StoreId = strStoreId, EF_Name = strName, EF_CAS = strCas, EF_Format = strFormat,
                EF_Amount = strAmount, EF_Price = strPrice, EF_Location = strLocation, EF_Saler = strSaler, EF_Note = strNote)

        jsonDict = {}
        jsonDict["id"] = newItem.id
        jsonDict["EF_TypeId"] = int(strTypeId)
        jsonDict["EF_StateId"] = int(strStateId)
        jsonDict["EF_PurityId"] = int(strPurityId)
        jsonDict["EF_UnitId"] = int(strUnitId)
        jsonDict["EF_StoreId"] = int(strStoreId)
        jsonDict["EF_Name"] = strName
        jsonDict["EF_CAS"] = strCas
        jsonDict["EF_Format"] = strFormat
        jsonDict["EF_Amount"] = strAmount
        jsonDict["EF_Price"] = float(strPrice)
        jsonDict["EF_Location"] = strLocation
        jsonDict["EF_Saler"] = strSaler
        jsonDict["EF_Note"] = strNote
        jsonStr = json.dumps(jsonDict, ensure_ascii=True) 

        return JsonResponse(jsonStr, status = 201, safe=False)

    def put(self, request):
        intCurId = int(request.PUT.get("id"))
        curItem = Matters.objects.get(id = intCurId)

        curItem.EF_TypeId = request.PUT.get("EF_TypeId", "") 
        curItem.EF_StateId = request.PUT.get("EF_StateId", "") 
        curItem.EF_PurityId = request.PUT.get("EF_PurityId", "") 
        curItem.EF_UniteId = request.PUT.get("EF_UnitId", "") 
        curItem.EF_StoreId = request.PUT.get("EF_StoreId", "") 
        curItem.EF_Name = request.PUT.get("EF_Name", "") 
        curItem.EF_CAS = request.PUT.get("EF_CAS", "") 
        curItem.EF_Format = request.PUT.get("EF_Format", "") 
        curItem.EF_Amount = request.PUT.get("EF_Amount", "") 
        curItem.EF_Price = request.PUT.get("EF_Price", "") 
        curItem.EF_Location = request.PUT.get("EF_Location", "") 
        curItem.EF_Saler = request.PUT.get("EF_Saler", "") 
        curItem.EF_Note = request.PUT.get("EF_Note", "") 
        curItem.save()

        jsonDict = {}
        jsonDict["id"] = curItem.id
        jsonDict["EF_TypeId"] = int(curItem.EF_TypeId)
        jsonDict["EF_StateId"] = int(curItem.EF_StateId)
        jsonDict["EF_PurityId"] = int(curItem.EF_PurityId)
        jsonDict["EF_UnitId"] = int(curItem.EF_UnitId)
        jsonDict["EF_StoreId"] = int(curItem.EF_StoreId)
        jsonDict["EF_Name"] = curItem.EF_Name
        jsonDict["EF_CAS"] = curItem.EF_CAS
        jsonDict["EF_Format"] = curItem.EF_Format
        jsonDict["EF_Amount"] = curItem.EF_Amount
        jsonDict["EF_Price"] = curItem.EF_Price
        jsonDict["EF_Location"] = curItem.EF_Location
        jsonDict["EF_Saler"] = curItem.EF_Saler
        jsonDict["EF_Note"] = curItem.EF_Note
        jsonStr = json.dumps(jsonDict, ensure_ascii=False) 

        return JsonResponse(jsonStr, status = 200, safe=False)

    def delete(self, request, intTypeId):
        curItem = Matters.objects.get(id = int(intTypeId))
        curItem.delete()
        return HttpResponse(status = 200)

    def to_json(self, objects):
        return serializers.serialize('json', objects)


#药品存量预警
class CMatterAlertsView(Resource):

    def get(self, request):
        strId = request.GET.get("id", "") 
        strMatterId = request.GET.get("EF_MatterId", "") 
        strYellowAmount = request.GET.get("EF_YellowAmount", "") 
        strRedAmount = request.GET.get("EF_RedAmount", "") 
        arrValidItems = MatterAlerts.objects.all() 

        if (strId != ""):
            arrValidItems = arrValidItems.filter(id__contains = int(strId))
        if (strMatterId != "" and strMatterId != "0"):
            arrValidItems = arrValidItems.filter(EF_MatterId__contains = strMatterId)
        if (strYellowAmount != ""):
            arrValidItems = arrValidItems.filter(EF_YellowAmount__contains = strYellowAmount)
        if (strRedAmount != ""):
            arrValidItems = arrValidItems.filter(EF_RedAmount__contains = strRedAmount)

        return HttpResponse(self.to_json(arrValidItems), content_type = 'application/json', status = 200)

    def post(self, request):
        strMatterId = request.POST.get("EF_MatterId", "") 
        strYellowAmount = request.POST.get("EF_YellowAmount", "") 
        strRedAmount = request.POST.get("EF_RedAmount", "") 
        newItem = MatterAlerts.objects.create(EF_MatterId = strMatterId, EF_YellowAmount = strYellowAmount,
                EF_RedAmount = strRedAmount)

        jsonDict = {}
        jsonDict["id"] = newItem.id
        jsonDict["EF_MatterId"] = int(newItem.EF_MatterId)
        jsonDict["EF_YellowAmount"] = int(newItem.EF_YellowAmount)
        jsonDict["EF_RedAmount"] = int(newItem.EF_RedAmount)
        jsonStr = json.dumps(jsonDict, ensure_ascii=True) 

        return JsonResponse(jsonStr, status = 201, safe=False)

    def put(self, request):
        intCurId = int(request.PUT.get("id"))
        curItem = MatterAlerts.objects.get(id = intCurId)
        curItem.EF_MatterId = request.PUT.get("EF_MatterId", "")
        curItem.EF_YellowAmount = request.PUT.get("EF_YellowAmount", "")
        curItem.EF_RedAmount = request.PUT.get("EF_RedAmount", "")
        curItem.save()

        jsonDict = {}
        jsonDict["id"] = curItem.id
        jsonDict["EF_MatterId"] = int(curItem.EF_MatterId)
        jsonDict["EF_YellowAmount"] = int(curItem.EF_YellowAmount)
        jsonDict["EF_RedAmount"] = int(curItem.EF_RedAmount)
        jsonStr = json.dumps(jsonDict, ensure_ascii=True) 

        return JsonResponse(jsonStr, status = 200, safe=False)

    def delete(self, request, intTypeId):
        curItem = MatterAlerts.objects.get(id = int(intTypeId))
        curItem.delete()
        return HttpResponse(status = 200)

    def to_json(self, objects):
        return serializers.serialize('json', objects)


#药品最小剩余量
class CMatterMinRemainsView(Resource):

    def get(self, request):
        strId = request.GET.get("id", "") 
        strMatterId = request.GET.get("EF_MatterId", "") 
        strStudentTypeId = request.GET.get("EF_StudentTypeId", "") 
        strMinRemain = request.GET.get("EF_MinRemain", "") 
        arrValidItems = MatterMinRemains.objects.all() 

        if (strId != ""):
            arrValidItems = arrValidItems.filter(id__contains = int(strId))
        if (strMatterId != "" and strMatterId != "0"):
            arrValidItems = arrValidItems.filter(EF_MatterId__contains = strMatterId)
        if (strStudentTypeId != "" and strStudentTypeId != "0"):
            arrValidItems = arrValidItems.filter(EF_StudentTypeId__contains = strStudentTypeId)
        if (strMinRemain != ""):
            arrValidItems = arrValidItems.filter(EF_MinRemain__contains = strMinRemain)

        return HttpResponse(self.to_json(arrValidItems), content_type = 'application/json', status = 200)

    def post(self, request):
        strMatterId = request.POST.get("EF_MatterId", "") 
        strStudentTypeId = request.POST.get("EF_StudentTypeId", "") 
        strMinRemain = request.POST.get("EF_MinRemain", "") 
        newItem = MatterMinRemains.objects.create(EF_MatterId = strMatterId, EF_StudentTypeId = strStudentTypeId,
                EF_MinRemain = strMinRemain)

        jsonDict = {}
        jsonDict["id"] = newItem.id
        jsonDict["EF_MatterId"] = int(newItem.EF_MatterId)
        jsonDict["EF_StudentTypeId"] = int(newItem.EF_StudentTypeId)
        jsonDict["EF_MinRemain"] = int(newItem.EF_MinRemain)
        jsonStr = json.dumps(jsonDict, ensure_ascii=True) 

        return JsonResponse(jsonStr, status = 201, safe=False)

    def put(self, request):
        intCurId = int(request.PUT.get("id"))
        curItem = MatterMinRemains.objects.get(id = intCurId)
        curItem.EF_MatterId = request.PUT.get("EF_MatterId", "")
        curItem.EF_StudentTypeId = request.PUT.get("EF_StudentTypeId", "")
        curItem.EF_MinRemain = request.PUT.get("EF_MinRemain", "")
        curItem.save()

        jsonDict = {}
        jsonDict["id"] = curItem.id
        jsonDict["EF_MatterId"] = int(curItem.EF_MatterId)
        jsonDict["EF_StudentTypeId"] = int(curItem.EF_StudentTypeId)
        jsonDict["EF_MinRemain"] = int(curItem.EF_MinRemain)
        jsonStr = json.dumps(jsonDict, ensure_ascii=True) 

        return JsonResponse(jsonStr, status = 200, safe=False)

    def delete(self, request, intTypeId):
        curItem = MatterMinRemains.objects.get(id = int(intTypeId))
        curItem.delete()
        return HttpResponse(status = 200)

    def to_json(self, objects):
        return serializers.serialize('json', objects)


#药品权限禁止
class CMatterAccessBlocksView(Resource):

    def get(self, request):
        strId = request.GET.get("id", "") 
        strMatterId = request.GET.get("EF_MatterId", "") 
        strStudentTypeId = request.GET.get("EF_StudentTypeId", "") 
        arrValidItems = MatterAccessBlocks.objects.all() 

        if (strId != ""):
            arrValidItems = arrValidItems.filter(id__contains = int(strId))
        if (strMatterId != "" and strMatterId != "0"):
            arrValidItems = arrValidItems.filter(EF_MatterId__contains = strMatterId)
        if (strStudentTypeId != "" and strStudentTypeId != "0"):
            arrValidItems = arrValidItems.filter(EF_StudentTypeId__contains = strStudentTypeId)

        return HttpResponse(self.to_json(arrValidItems), content_type = 'application/json', status = 200)

    def post(self, request):
        strMatterId = request.POST.get("EF_MatterId", "") 
        strStudentTypeId = request.POST.get("EF_StudentTypeId", "") 
        newItem = MatterAccessBlocks.objects.create(EF_MatterId = strMatterId, EF_StudentTypeId = strStudentTypeId)

        jsonDict = {}
        jsonDict["id"] = newItem.id
        jsonDict["EF_MatterId"] = int(newItem.EF_MatterId)
        jsonDict["EF_StudentTypeId"] = int(newItem.EF_StudentTypeId)
        jsonStr = json.dumps(jsonDict, ensure_ascii=True) 

        return JsonResponse(jsonStr, status = 201, safe=False)

    def put(self, request):
        intCurId = int(request.PUT.get("id"))
        curItem = MatterAccessBlocks.objects.get(id = intCurId)
        intOldTypeId = curItem.EF_StudentTypeId
        curItem.EF_MatterId = request.PUT.get("EF_MatterId", "")
        curItem.EF_StudentTypeId = request.PUT.get("EF_StudentTypeId", "")
        curItem.save()

        #若类型改变了，则删除其相关表的信息
        if (intOldTypeId != curItem.EF_StudentTypeId):
            subItemList = SubMatterAccessBlocks.objects.all().filter(EF_BlockId = intCurId)
            for index in subItemList:
                index.delete()

        jsonDict = {}
        jsonDict["id"] = curItem.id
        jsonDict["EF_MatterId"] = int(curItem.EF_MatterId)
        jsonDict["EF_StudentTypeId"] = int(curItem.EF_StudentTypeId)
        jsonStr = json.dumps(jsonDict, ensure_ascii=True) 

        return JsonResponse(jsonStr, status = 200, safe=False)

    def delete(self, request, intTypeId):
        curItem = MatterAccessBlocks.objects.get(id = int(intTypeId))

        #删除其相关表的信息
        subItemList = SubMatterAccessBlocks.objects.all().filter(EF_BlockId = intTypeId)
        for index in subItemList:
            index.delete()

        curItem.delete()
        return HttpResponse(status = 200)

    def to_json(self, objects):
        return serializers.serialize('json', objects)


#学生药品权限禁止
class CSubMatterAccessBlocksView(Resource):

    def get(self, request):
        strId = request.GET.get("id", "") 
        strBlockId = request.GET.get("EF_BlockId", "") 
        strStudentId = request.GET.get("EF_StudentId", "") 
        arrValidItems = SubMatterAccessBlocks.objects.all() 

        if (strId != ""):
            arrValidItems = arrValidItems.filter(id__contains = int(strId))
        if (strBlockId != "" and strBlockId != "0"):
            arrValidItems = arrValidItems.filter(EF_BlockId__contains = strBlockId)
        if (strStudentId != "" and strStudentId != "0"):
            arrValidItems = arrValidItems.filter(EF_StudentId__contains = strStudentId)

        return HttpResponse(self.to_json(arrValidItems), content_type = 'application/json', status = 200)

    def post(self, request):
        strBlockId = request.POST.get("EF_BlockId", "") 
        strStudentId = request.POST.get("EF_StudentId", "") 
        newItem = SubMatterAccessBlocks.objects.create(EF_BlockId = strBlockId, EF_StudentId = strStudentId)

        jsonDict = {}
        jsonDict["id"] = newItem.id
        jsonDict["EF_BlockId"] = int(newItem.EF_BlockId)
        jsonDict["EF_StudentId"] = int(newItem.EF_StudentId)
        jsonStr = json.dumps(jsonDict, ensure_ascii=True) 

        return JsonResponse(jsonStr, status = 201, safe=False)

    def put(self, request):
        intCurId = int(request.PUT.get("id"))
        curItem = SubMatterAccessBlocks.objects.get(id = intCurId)
        curItem.EF_BlockId = request.PUT.get("EF_BlockId", "")
        curItem.EF_StudentId = request.PUT.get("EF_StudentId", "")
        curItem.save()

        jsonDict = {}
        jsonDict["id"] = curItem.id
        jsonDict["EF_BlockId"] = int(curItem.EF_BlockId)
        jsonDict["EF_StudentId"] = int(curItem.EF_StudentId)
        jsonStr = json.dumps(jsonDict, ensure_ascii=True) 

        return JsonResponse(jsonStr, status = 200, safe=False)

    def delete(self, request, intTypeId):
        curItem = SubMatterAccessBlocks.objects.get(id = int(intTypeId))
        curItem.delete()
        return HttpResponse(status = 200)

    def to_json(self, objects):
        return serializers.serialize('json', objects)




