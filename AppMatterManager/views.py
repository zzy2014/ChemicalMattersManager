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


def calculateCensorePattern(request):
    userDict = getCurUser(request)
    curUser = userDict["curUser"]
    if (curUser == ""):
        return HttpResponse("当前用户不存在或未登录！", status = 403)

    #如果当前用户为学生，则应添加其导师
    arrValues = []
    if (userDict["type"] == "Student"):
        arrValues.append("教师")

    #并检查是否存在有毒，燃，爆的类型
    bIsDangerous = False;
    arrValidItems = MatterDetails.objects.all().filter(EF_ImportFormId = 0)
    for item in arrValidItems:
        if (bIsDangerous):
            break
        else:
            curMatter = Matters.objects.get(id = item.EF_MatterId)
            bIsDangerous = (curMatter.EF_TypeId != 1)

    if (bIsDangerous):
        arrValues.append("院长")
    else:
        arrValues.append("副院长")
    
    strField = "EF_TypeName__in"
    strCondition = {strField:arrValues}
    arrCensoreTypeIds = UserTypes.objects.all().filter(**strCondition);

    #确定审核模型ID
    arrCensorePatterns = CensorePatterns.objects.all().filter(EF_StepsCount = len(arrCensoreTypeIds))

    nIndex = 0
    for item in arrCensoreTypeIds:
        nIndex += 1
        strField = "EF_UserTypeId%d" %(nIndex)
        strCondition = {strField:item.id}
        arrCensorePatterns = arrCensorePatterns.filter(**strCondition)

        
    #设置入库单的审核ID
    if (len(arrCensorePatterns) < 1):
        return HttpResponse("没有审核人！", status = 403)

    #将审核模型写入session
    request.session['censorePatternId'] = arrCensorePatterns[0].id
    request.session.set_expiry(0)


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


def createNewImportForm(request):
    userDict = getCurUser(request)
    curUser = userDict["curUser"]
    if (curUser == ""):
        return HttpResponse("当前用户不存在或未登录！")

    #从session中获取己计算出的审核模型ID
    censorePatternId = request.session.get('censorePatternId', default=0)
    del request.session['censorePatternId']

    #获取用户选择的第一个审核人
    censoreUserId = 0
    if request.method == 'POST' :
        censoreUserId = request.POST.get('censoreUserId')

    #获取当前时间，并格式化为数据库中格式
    timeNow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    #创建一个新的入库单
    newForm = ImportForms.objects.create(EF_UserTypeId = userDict["typeId"], EF_UserId = userDict["id"],
            EF_FormStateId = "1", EF_Time = timeNow, EF_CensorePatternId = censorePatternId,
            EF_UserId1 = censoreUserId, EF_CensoreStateId1 = 6)

    #更新临时的药品明细列表中的入库单ID
    arrValidItems = MatterDetails.objects.all().filter(EF_ImportFormId = 0)
    for item in arrValidItems:
        item.EF_ImportFormId = newForm.id
        item.save()

    return JsonResponse({'retCode':1})


#执行审核
def showCensoreDialog(request):
    userDict = getCurUser(request)
    curUser = userDict["curUser"]
    if (curUser == ""):
        return HttpResponse("当前用户不存在或未登录！", status = 403)

    if request.method != 'POST' :
        return HttpResponse("访问方法不正确！", status = 403)

    curCensoreUserTypeId =  request.POST.get('curCensoreUserTypeId')
    curCensoreUserId =  request.POST.get('curCensoreUserId')
    #判断当前用户是否为审核用户
    if (int(curCensoreUserTypeId) != int(userDict["typeId"]) or int(curCensoreUserId) != int(userDict["id"])):
        return HttpResponse("您无权代替他人进行审核！", status = 403)

    curCensoreStateId =  request.POST.get('curCensoreStateId')
    nextUserTypeId =  request.POST.get('nextUserTypeId')

    #获取所有的审核状态
    censoreStates =  CensoreStates.objects.all()

    #获取下一个人
    strNextCensoreType = ""
    arrCensores = []
    if (nextUserTypeId != "" and int(nextUserTypeId) > 0):
        strNextCensoreType = UserTypes.objects.get(id = nextUserTypeId).EF_TypeName;
        if (strNextCensoreType == SuperAdministrators.Type):
            arrCensores = SuperAdministrators.objects.all()
        elif (strNextCensoreType == Administrators.Type):
            arrCensores = Administrators.objects.all()
        elif (strNextCensoreType == ChiefCollegeLeaders.Type):
            arrCensores = ChiefCollegeLeaders.objects.all()
        elif (strNextCensoreType == CollegeLeaders.Type):
            arrCensores = CollegeLeaders.objects.all()
        elif (strNextCensoreType == Teachers.Type):
            arrCensores = Teachers.objects.all()

    #将当前审核的入库单ID和审核的用户列名写入session
    request.session['curImportFormId'] = request.POST.get('curImportFormId')
    request.session['curUserIndexId'] = request.POST.get('curUserIndexId')
    request.session.set_expiry(0)


    context = {} #一个字典对象
    context['censoreStates'] =  censoreStates#传入模板中的变量
    context['nextCensoreTypeName'] =  strNextCensoreType#传入模板中的变量
    context['arrCensores'] = arrCensores #传入模板中的变量
    return render_to_response("showCensoreDialog.html", context, status = 200)

def censoreImportForm(request):
    userDict = getCurUser(request)
    curUser = userDict["curUser"]
    if (curUser == ""):
        return HttpResponse("当前用户不存在或未登录！", status = 403)

    if request.method != 'POST' :
        return HttpResponse("访问方法不正确！", status = 403)

    #从session中获取当前入库单id和用户所属列
    curImportFormId = int(request.session.get('curImportFormId', default=0))
    curUserIndexId = int(request.session.get('curUserIndexId', default=0))
    del request.session['curImportFormId']
    del request.session['curUserIndexId']

    if (curImportFormId < 1 or curUserIndexId < 1):
        return HttpResponse("入库单无效！", status = 403)

    #获取当前选中的审核状态、下一个审核人与评论
    selCensoreStateId = int(request.POST.get('censoreStateId'))
    if (selCensoreStateId < 1):
        return HttpResponse("状态无效！", status = 403)

    nextCensoreUserId = int(request.POST.get('nextCensoreUserId'))
    strComment =  request.POST.get('strComment')

    #设置当前入库单信息
    curImportForm = ImportForms.objects.get(id = curImportFormId)
    strCurCensoreStateField = "EF_CensoreStateId%d"%(curUserIndexId)
    setattr(curImportForm, strCurCensoreStateField, selCensoreStateId);
    strCurCommentField = "EF_CensoreComment%d"%(curUserIndexId)
    setattr(curImportForm, strCurCommentField, strComment)

    strNextUserIdField = "EF_UserId%d"%(curUserIndexId+1)
    strNextCensoreStateIdField = "EF_CensoreStateId%d"%(curUserIndexId+1)

    #审核通过则传递给下一个，并置状态为审核中
    if (selCensoreStateId == 3):
        setattr(curImportForm, strNextUserIdField, nextCensoreUserId)
        setattr(curImportForm, strNextCensoreStateIdField, 6)
        if (nextCensoreUserId > 0):
            setattr(curImportForm, "EF_FormStateId", 2)
        else:
            setattr(curImportForm, "EF_FormStateId", 4)
    #审核未通过，则不进行传递，且置状态为己拒绝
    elif (selCensoreStateId == 5):
        setattr(curImportForm, strNextUserIdField, 0)
        setattr(curImportForm, strNextCensoreStateIdField, 0)
        setattr(curImportForm, "EF_FormStateId", 5)

    curImportForm.save()

    return HttpResponse("审核成功！", None, 200)
