# coding=utf8
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render, render_to_response
from simple_rest import Resource #第三方的小类
from django.core import serializers #导入序列化
from django.core.files.base import ContentFile
import json
import datetime
from AppUserManager.models import UserTypes, SuperAdministrators, Administrators, ChiefCollegeLeaders, CollegeLeaders, Teachers
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
    elif (strPageType == "showCensorePatterns"):
        return render_to_response("showOneTable.html", context)
    elif (strPageType == "showFormStates"):
        return render_to_response("showOneTable.html", context)
    elif (strPageType == "addMatterDetails"):
        return render_to_response("showOneTableTwoBtns.html", context)
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

    if (strPageType == "showImportForms"):
        return render_to_response("showTwoTables.html", context)
    else:
        return HttpResponse("")


#审核状态
class CCensoreStatesView(Resource):

    def get(self, request):
        strId = request.GET.get("id", "") 
        strName = request.GET.get("EF_StateName", "") 
        arrValidItems = CensoreStates.objects.all() 

        if (strId != ""):
            arrValidItems = arrValidItems.filter(id__contains = int(strId))
        if (strName != ""):
            arrValidItems = arrValidItems.filter(EF_StateName__contains = strName)

        return HttpResponse(self.to_json(arrValidItems), content_type = 'application/json', status = 200)

    def post(self, request):
        strName = request.POST.get("EF_StateName", "")
        newItem = CensoreStates.objects.create(EF_StateName = strName)
        return JsonResponse({"id":newItem.id,"EF_StateName":newItem.EF_StateName}, status = 201)

    def put(self, request):
        intCurId = int(request.PUT.get("id"))
        curItem = CensoreStates.objects.get(id = intCurId)
        curItem.EF_StateName= request.PUT.get("EF_StateName", "")
        curItem.save()
        return JsonResponse({"id":curItem.id, "EF_StateName":curItem.EF_StateName}, status = 200)

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
        strStepsCount = request.GET.get("EF_StepsCount", "") 
        strUserTypeId1 = request.GET.get("EF_UserTypeId1", "") 
        strUserTypeId2 = request.GET.get("EF_UserTypeId2", "") 
        strUserTypeId3 = request.GET.get("EF_UserTypeId3", "") 
        arrValidItems = CensorePatterns.objects.all() 

        if (strId != ""):
            arrValidItems = arrValidItems.filter(id__contains = int(strId))
        if (strStepsCount != "" and strStepsCount != "0"):
            arrValidItems = arrValidItems.filter(EF_StepsCount__contains = strStepsCount)
        if (strUserTypeId1 != "" and strUserTypeId1 != "0"):
            arrValidItems = arrValidItems.filter(EF_UserTypeId1__contains = strUserTypeId1)
        if (strUserTypeId2 != "" and strUserTypeId2 != "0"):
            arrValidItems = arrValidItems.filter(EF_UserTypeId2__contains = strUserTypeId2)
        if (strUserTypeId3 != "" and strUserTypeId3 != "0"):
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
        intCurId = int(request.PUT.get("id", "0"))
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
        jsonDict["id"] = intCurId
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


#单据状态
class CFormStatesView(Resource):

    def get(self, request):
        strId = request.GET.get("id", "") 
        strName = request.GET.get("EF_StateName", "") 
        arrValidItems = FormStates.objects.all() 

        if (strId != ""):
            arrValidItems = arrValidItems.filter(id__contains = int(strId))
        if (strName != ""):
            arrValidItems = arrValidItems.filter(EF_StateName__contains = strName)

        return HttpResponse(self.to_json(arrValidItems), content_type = 'application/json', status = 200)

    def post(self, request):
        strName = request.POST.get("EF_StateName", "")
        newItem = FormStates.objects.create(EF_StateName = strName)
        return JsonResponse({"id":newItem.id,"EF_StateName":newItem.EF_StateName}, status = 201)

    def put(self, request):
        intCurId = int(request.PUT.get("id"))
        curItem = FormStates.objects.get(id = intCurId)
        curItem.EF_StateName= request.PUT.get("EF_StateName", "")
        curItem.save()
        return JsonResponse({"id":curItem.id, "EF_StateName":curItem.EF_StateName}, status = 200)

    def delete(self, request, intTypeId):
        curItem = FormStates.objects.get(id = int(intTypeId))
        curItem.delete()
        return HttpResponse(status = 200)

    def to_json(self, objects):
        return serializers.serialize('json', objects)

#从MatterDetails中删除所有ImportFormId=0的临时数据
def delTempMatterDetails(request):
    userDict = getCurUser(request)
    curUser = userDict["curUser"]
    if (curUser == ""):
        return JsonResponse({"retCode":-1})

    arrValidItems = MatterDetails.objects.filter(EF_ImportFormId=0).delete()
    return JsonResponse({"retCode":1})


#入库操作
class CAddMatterDetailsView(Resource):

    def get(self, request):
        strId = request.GET.get("id", "") 
        strFormId = request.GET.get("EF_ImportFormId", "") 
        strMatterId = request.GET.get("EF_MatterId", "") 
        strCount = request.GET.get("EF_MatterCount", "") 
        arrValidItems = MatterDetails.objects.all() 

        if (strId != ""):
            arrValidItems = arrValidItems.filter(id__contains = int(strId))
        if (strFormId != ""):
            arrValidItems = arrValidItems.filter(EF_ImportFormId = strFormId)
        if (strMatterId != "" and strMatterId != "0"):
            arrValidItems = arrValidItems.filter(EF_MatterId__contains = strMatterId)
        if (strCount != ""):
            arrValidItems = arrValidItems.filter(EF_MatterCount__contains = strCount)

        return HttpResponse(self.to_json(arrValidItems), content_type = 'application/json', status = 200)

    def post(self, request):
        strFormId = request.POST.get("EF_ImportFormId", "") 
        strMatterId = request.POST.get("EF_MatterId", "") 
        strCount = request.POST.get("EF_MatterCount", "") 

        newItem = MatterDetails.objects.create(EF_ImportFormId = strFormId, EF_MatterId = strMatterId,
                EF_MatterCount = strCount)

        jsonDict = {}
        jsonDict["id"] = newItem.id
        jsonDict["EF_ImportFormId"] = int(strFormId)
        jsonDict["EF_MatterId"] = int(strMatterId)
        jsonDict["EF_MatterCount"] = int(strCount)
        jsonStr = json.dumps(jsonDict, ensure_ascii=True) 

        return JsonResponse(jsonStr, status = 201, safe=False)

    def put(self, request):
        intCurId = int(request.PUT.get("id"))
        curItem = MatterDetails.objects.get(id = intCurId)
        curItem.EF_ImportFormId = int(request.PUT.get("EF_ImportFormId"))
        curItem.EF_MatterId= request.PUT.get("EF_MatterId", "")
        curItem.EF_MatterCount= request.PUT.get("EF_MatterCount", "")
        curItem.save()

        jsonDict = {}
        jsonDict["id"] = curItem.id
        jsonDict["EF_ImportFormId"] = int(curItem.EF_ImportFormId)
        jsonDict["EF_MatterId"] = int(curItem.EF_MatterId)
        jsonDict["EF_MatterCount"] = int(curItem.EF_MatterCount)
        jsonStr = json.dumps(jsonDict, ensure_ascii=True) 

        return JsonResponse(jsonStr, status = 200, safe=False)

    def delete(self, request, intTypeId):
        curItem = MatterDetails.objects.get(id = int(intTypeId))
        curItem.delete()
        return HttpResponse(status = 200)

    def to_json(self, objects):
        return serializers.serialize('json', objects)


def upLoadImportForm(request):
    userDict = getCurUser(request)
    curUser = userDict["curUser"]
    if (curUser == ""):
        return HttpResponse("当前用户不存在或未登录！")

    #获取当前时间，并格式化为数据库中格式
    timeNow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    #创建一个新的入库单
    newForm = ImportForms.objects.create(EF_UserTypeId = userDict["typeId"], EF_UserId = userDict["id"],
            EF_FormStateId = "1", EF_Time = timeNow)


    #更新临时的药品明细列表中的入库单ID
    #并检查是否存在有毒，燃，爆的类型
    bIsDangerous = False;
    arrValidItems = MatterDetails.objects.all().filter(EF_ImportFormId = 0)
    for item in arrValidItems:
        item.EF_ImportFormId = newForm.id
        item.save()
        if (not bIsDangerous):
            curMatter = Matters.objects.get(id = item.EF_MatterId)
            print(curMatter.EF_TypeId)
            bIsDangerous = (curMatter.EF_TypeId != 1)

    #确定审核模型ID
    arrCensoreTypeIds = UserTypes.objects.all();
    if (bIsDangerous):
        arrCensoreTypeIds = arrCensoreTypeIds.filter(EF_TypeName = "院长")
    else:
        arrCensoreTypeIds = arrCensoreTypeIds.filter(EF_TypeName = "副院长")

    arrCensorePatterns = CensorePatterns.objects.all();
    arrCensorePatterns = arrCensorePatterns.filter(EF_StepsCount = len(arrCensoreTypeIds))
    nIndex = 0
    for item in arrCensoreTypeIds:
        nIndex += 1
        strField = "EF_UserTypeId%d" %(nIndex)
        strCondition = {strField:item.id}
        arrCensorePatterns = arrCensorePatterns.filter(**strCondition)

        
    #设置入库单的审核ID
    if (len(arrCensorePatterns) < 1):
        return HttpResponse("没有审核人！")

    newForm.EF_CensorePatternId = arrCensorePatterns[0].id
    newForm.save();

    #获取第一个审核人
    arrCensores = []
    strFirstCensoreType = UserTypes.objects.get(id = arrCensoreTypeIds[0].id).EF_TypeName
    if (strFirstCensoreType == SuperAdministrators.Type):
        arrCensores = SuperAdministrators.objects.all()
    elif (strFirstCensoreType == Administrators.Type):
        arrCensores = Administrators.objects.all()
    elif (strFirstCensoreType == ChiefCollegeLeaders.Type):
        arrCensores = ChiefCollegeLeaders.objects.all()
    elif (strFirstCensoreType == CollegeLeaders.Type):
        arrCensores = CollegeLeaders.objects.all()
    elif (strFirstCensoreType == Teachers.Type):
        arrCensores = Teachers.objects.all()

    context = {} #一个字典对象
    context['censoreTypeName'] =  strFirstCensoreType#传入模板中的变量
    context['arrCensores'] = arrCensores #传入模板中的变量
    return render_to_response("censoreOption.html", context)


#入库清单
class CImportFormsView(Resource):

    def get(self, request):
        strId = request.GET.get("id", "") 
        strUserTypeId = request.GET.get("EF_UserTypeId", "") 
        strUserId = request.GET.get("EF_UserId", "") 
        strFormStateId = request.GET.get("EF_FormStateId", "") 
        strTime = request.GET.get("EF_Time", "") 
        strCensore1 = request.GET.get("EF_UserId1", "") 
        strCensoreState1 = request.GET.get("EF_CensoreStateId1", "") 
        strCensoreComment1 = request.GET.get("EF_CensoreComment1", "") 
        strCensore2 = request.GET.get("EF_UserId2", "") 
        strCensoreState2 = request.GET.get("EF_CensoreStateId2", "") 
        strCensoreComment2 = request.GET.get("EF_CensoreComment2", "") 
        strCensore3 = request.GET.get("EF_UserId3", "") 
        strCensoreState3 = request.GET.get("EF_CensoreStateId3", "") 
        strCensoreComment3 = request.GET.get("EF_CensoreComment3", "") 

        arrValidItems = ImportForms.objects.all() 

        if (strId != ""):
            arrValidItems = arrValidItems.filter(id__contains = int(strId))
        if (strUserTypeId != ""):
            arrValidItems = arrValidItems.filter(EF_UserTypeId__contains = strUserTypeId)
        if (strUserId != ""):
            arrValidItems = arrValidItems.filter(EF_UserId__contains = strUserId)
        if (strFormStateId != ""):
            arrValidItems = arrValidItems.filter(EF_FormStateId__contains = strFormStateId)
        if (strTime != ""):
            arrValidItems = arrValidItems.filter(EF_Time__contains = strTime)
        if (strCensore1 != ""):
            arrValidItems = arrValidItems.filter(EF_UserId1__contains = strCensore1)
        if (strCensoreState1 != ""):
            arrValidItems = arrValidItems.filter(EF_CensoreStateId1__contains = strCensoreState1)
        if (strCensoreComment1 != ""):
            arrValidItems = arrValidItems.filter(EF_CensoreComment1__contains = strCensoreComment1)
        if (strCensore2 != ""):
            arrValidItems = arrValidItems.filter(EF_UserId2__contains = strCensore2)
        if (strCensoreState2 != ""):
            arrValidItems = arrValidItems.filter(EF_CensoreStateId2__contains = strCensoreState2)
        if (strCensoreComment2 != ""):
            arrValidItems = arrValidItems.filter(EF_CensoreComment2__contains = strCensoreComment2)
        if (strCensore3 != ""):
            arrValidItems = arrValidItems.filter(EF_UserId3__contains = strCensore3)
        if (strCensoreState3 != ""):
            arrValidItems = arrValidItems.filter(EF_CensoreStateId3__contains = strCensoreState3)
        if (strCensoreComment3 != ""):
            arrValidItems = arrValidItems.filter(EF_CensoreComment3__contains = strCensoreComment3)

        return HttpResponse(self.to_json(arrValidItems), content_type = 'application/json', status = 200)

    def post(self, request):
        #不可修改
        return JsonResponse(jsonStr, status = 201, safe=False)

    def put(self, request):
        #新增
        return JsonResponse(jsonStr, status = 200, safe=False)

    def delete(self, request, intTypeId):
        curItem = ImportForms.objects.get(id = int(intTypeId))
        
        #删除相对应的药品明细
        subItemList = MatterDetails.objects.all().filter(EF_ImportFormId = intTypeId)
        for index in subItemList:
            index.delete()

        curItem.delete()
        return HttpResponse(status = 200)

    def to_json(self, objects):
        return serializers.serialize('json', objects)

