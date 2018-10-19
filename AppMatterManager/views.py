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
from .models import CensorePatterns, CensoreStates, FormStates, ImportForms, ImportMatterDetails
from .models import ExportForms, ExportMatterDetails, PerchaseForms, PerchaseMatterDetails, ReserveMatterDetails, ReserveForms

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
    elif (strPageType == "importMatterDetails"):
        context["btnText"] = "载入预采购单" 
        return render_to_response("showOneTablesTwoBtns.html", context)
    elif (strPageType == "exportMatterDetails"):
        context["btnText"] = "载入预约单" 
        return render_to_response("showOneTablesTwoBtns.html", context)
    elif (strPageType == "perchaseMatterDetails"):
        context["btnText"] = "导入文件" 
        return render_to_response("showOneTablesTwoBtns.html", context)
    elif (strPageType == "reserveMatterDetails"):
        context["btnText"] = "导入文件" 
        return render_to_response("showOneTablesTwoBtns.html", context)
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


#根据表名获取表对象
def getFormObject(strTableName):
    if (strTableName == ""):
        return ""
    elif (strTableName == "ImportMatterDetails"):
        return ImportMatterDetails
    elif (strTableName == "ExportMatterDetails"):
        return ExportMatterDetails
    elif (strTableName == "PerchaseMatterDetails"):
        return PerchaseMatterDetails
    elif (strTableName == "ReserveMatterDetails"):
        return ReserveMatterDetails
    elif (strTableName == "ImportForms"):
        return ImportForms
    elif (strTableName == "ExportForms"):
        return ExportForms
    elif (strTableName == "PerchaseForms"):
        return PerchaseForms
    elif (strTableName == "ReserveForms"):
        return ReserveForms
    else:
        return ""
 

#从表中删除指定条件的数据
def deleteFromOneTable(request):
    userDict = getCurUser(request)
    curUser = userDict["curUser"]
    if (curUser == ""):
        return HttpResponse("删除失败！", status = 403)

    if request.method != 'POST' :
        return HttpResponse("访问方法出错！", status = 403)

    #通过表名获取数据库对象
    curModel = getFormObject(request.POST.get("tableName"))
    if (curModel == ""):
        return HttpResponse("传入的数据表名无效！", status = 403)

    strFieldMethod = request.POST.get("fieldMethod") 
    methodValues = request.POST.get("methodValue") 
    condition = {strFieldMethod:methodValues}

    curModel.objects.all().filter(**condition).delete();

    return HttpResponse("删除成功！")


#计算出当前临时材料的审核类型
def calculateCensorePattern(request):
    userDict = getCurUser(request)
    curUser = userDict["curUser"]
    if (curUser == ""):
        return HttpResponse("当前用户不存在或未登录！", status = 403)

    if request.method != 'POST' :
        return HttpResponse("访问方法出错！", status = 403)

    #通过表名获取数据库对象
    strTableName = request.POST.get("tableName")
    curModel = getFormObject(strTableName)
    if (curModel == ""):
        return HttpResponse("传入的数据表名无效！", status = 403)

    #如果当前用户为学生，则应添加其导师
    arrValues = []
    if (userDict["type"] == "Student"):
        arrValues.append("教师")

    #并检查是否存在有毒，燃，爆的类型
    bIsDangerous = False;
    arrValidItems = curModel.objects.all().filter(EF_FormId = 0)
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

    #获取当前的对应的js
    jsFileName = ""
    if (strTableName == "ImportMatterDetails"):
        jsFileName = "importFirstCensoreOption"
    elif (strTableName == "ExportMatterDetails"):
        jsFileName = "exportFirstCensoreOption"
    elif (strTableName == "PerchaseMatterDetails"):
        jsFileName = "perchaseFirstCensoreOption"
    elif (strTableName == "ReserveMatterDetails"):
        jsFileName = "reserveFirstCensoreOption"


    context = {} #一个字典对象
    context['censoreTypeName'] =  strFirstCensoreType#传入模板中的变量
    context['arrCensores'] = arrCensores #传入模板中的变量
    context['jsFileName'] = jsFileName #传入模板中的变量
    return render_to_response("firstCensoreOption.html", context)


#创建新的表单
def createNewForm(request):
    userDict = getCurUser(request)
    curUser = userDict["curUser"]
    if (curUser == ""):
        return HttpResponse("当前用户不存在或未登录！", status = 403)

    if request.method != 'POST' :
        return HttpResponse("访问方法出错！", status = 403)

    #通过表名获取数据库对象
    curFormModel = getFormObject(request.POST.get("formTableName"))
    if (curFormModel == ""):
        return HttpResponse("传入的数据表名无效！", status = 403)

    curDetailModel = getFormObject(request.POST.get("detailTableName"))
    if (curDetailModel == ""):
        return HttpResponse("传入的材料信息数据表名无效！", status = 403)


    #从session中获取己计算出的审核模型ID
    censorePatternId = request.session.get('censorePatternId', default=0)
    del request.session['censorePatternId']

    #获取用户选择的第一个审核人
    censoreUserId = request.POST.get('censoreUserId')

    #获取当前时间，并格式化为数据库中格式
    timeNow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    #创建一个新的入库单
    newForm = curFormModel.objects.create(EF_UserTypeId = userDict["typeId"], EF_UserId = userDict["id"],
            EF_FormStateId = "1", EF_Time = timeNow, EF_CensorePatternId = censorePatternId,
            EF_UserId1 = censoreUserId, EF_CensoreStateId1 = 6)

    #更新临时的药品明细列表中的入库单ID
    arrValidItems = curDetailModel.objects.all().filter(EF_FormId = 0)
    for item in arrValidItems:
        item.EF_FormId = newForm.id
        item.save()

    return HttpResponse("添加成功！")


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
    request.session['curFormTableName'] = request.POST.get('curFormTableName')
    request.session['curFormId'] = request.POST.get('curFormId')
    request.session['curUserIndexId'] = request.POST.get('curUserIndexId')
    request.session.set_expiry(0)


    context = {} #一个字典对象
    context['censoreStates'] =  censoreStates#传入模板中的变量
    context['nextCensoreTypeName'] =  strNextCensoreType#传入模板中的变量
    context['arrCensores'] = arrCensores #传入模板中的变量
    return render_to_response("censoreDialog.html", context, status = 200)


def censoreForm(request):
    userDict = getCurUser(request)
    curUser = userDict["curUser"]
    if (curUser == ""):
        return HttpResponse("当前用户不存在或未登录！", status = 403)

    if request.method != 'POST' :
        return HttpResponse("访问方法不正确！", status = 403)

    #从session中获取当前入库单id和用户所属列
    curFormTableName = request.session.get('curFormTableName', default="")
    curFormId = int(request.session.get('curFormId', default=0))
    curUserIndexId = int(request.session.get('curUserIndexId', default=0))
    del request.session['curFormTableName']
    del request.session['curFormId']
    del request.session['curUserIndexId']

    if (curFormTableName == "" or curFormId < 1 or curUserIndexId < 1):
        return HttpResponse("清单无效！", status = 403)

    #获取当前选中的审核状态、下一个审核人与评论
    selCensoreStateId = int(request.POST.get('censoreStateId'))
    if (selCensoreStateId < 1):
        return HttpResponse("状态无效！", status = 403)

    nextCensoreUserId = int(request.POST.get('nextCensoreUserId'))
    strComment =  request.POST.get('strComment')

    #通过表名获取数据库对象
    curFormModel = getFormObject(curFormTableName)
    if (curFormModel == ""):
        return HttpResponse("传入的数据表名无效！", status = 403)

    curFormItem = curFormModel.objects.get(id = curFormId)
    strCurCensoreStateField = "EF_CensoreStateId%d"%(curUserIndexId)
    setattr(curFormItem, strCurCensoreStateField, selCensoreStateId);
    strCurCommentField = "EF_CensoreComment%d"%(curUserIndexId)
    setattr(curFormItem, strCurCommentField, strComment)

    strNextUserIdField = "EF_UserId%d"%(curUserIndexId+1)
    strNextCensoreStateIdField = "EF_CensoreStateId%d"%(curUserIndexId+1)

    #审核通过则传递给下一个，并置状态为审核中
    if (selCensoreStateId == 3):
        if (nextCensoreUserId > 0):
            setattr(curFormItem, strNextUserIdField, nextCensoreUserId)
            setattr(curFormItem, strNextCensoreStateIdField, 6)
            setattr(curFormItem, "EF_FormStateId", 2)
        else:
            setattr(curFormItem, "EF_FormStateId", 3)
    #审核未通过，则不进行传递，且置状态为己拒绝
    elif (selCensoreStateId == 5):
        setattr(curFormItem, strNextUserIdField, 0)
        setattr(curFormItem, strNextCensoreStateIdField, 0)
        setattr(curFormItem, "EF_FormStateId", 5)

    curFormItem.save()

    return HttpResponse("审核成功！", None, 200)


#获取单据界面
def formOption(request):
    userDict = getCurUser(request)
    curUser = userDict["curUser"]
    if (curUser == ""):
        return HttpResponse("用户未登录或无效！", status = 403)

    if request.method != 'POST' :
        return HttpResponse("访问方法不正确！", status = 403)

    context = {} #一个字典对象
    context['jsFileName'] = request.POST.get("jsFileName", "") 
    return render_to_response("formOption.html", context, status = 200)


#从一个材料清单表中向另一个表中复制数据
def copyMatterDetails(request):
    userDict = getCurUser(request)
    curUser = userDict["curUser"]
    if (curUser == ""):
        return HttpResponse("用户未登录或无效！", status = 403)

    if request.method != 'POST' :
        return HttpResponse("访问方法不正确！", status = 403)

    fromTable = getFormObject(request.POST.get("fromTableName", ""))
    toTable = getFormObject(request.POST.get("toTableName", ""))
    if (fromTable == "" or toTable == ""):
        return HttpResponse("传入的表名有误！", status = 403)

    fromTableFormId = request.POST.get("fromTableFormId", 0)
    toTableFormId = request.POST.get("toTableFormId", 0)

    arrFromItems = fromTable.objects.all().filter(EF_FormId = fromTableFormId)
    for item in arrFromItems:
        toTable.objects.create(EF_FormId = toTableFormId, EF_MatterId = item.EF_MatterId, EF_MatterCount = item.EF_MatterCount)

    return HttpResponse("复制完成")


#生成己满足条件的预采购材料列表
def genPerchaseMatterDetails(request):
    userDict = getCurUser(request)
    curUser = userDict["curUser"]
    if (curUser == ""):
        return HttpResponse("用户未登录或无效！", status = 403)

    #删除旧的临时数据
    PerchaseMatterDetails.objects.all().filter(EF_FormId = 0).delete();

    #创建所有的
    arrCandidates = MatterMinRemains.objects.all()
    for item in arrCandidates:
        curMatter = Matters.objects.get(id = item.EF_MatterId)
        intNeedAmount = item.EF_MinRemain - curMatter.EF_Amount
        if (intNeedAmount < 1):
            continue

        newPerchaseItem = PerchaseMatterDetails.objects.create(EF_FormId = 0, EF_MatterId = item.EF_MatterId,
                EF_MatterCount = intNeedAmount)

    return HttpResponse("初始化采购单成功！")



#预采购操作
class CPerchaseMatterDetailsView(Resource):

    def get(self, request):
        strId = request.GET.get("id", "") 
        strFormId = request.GET.get("EF_FormId", "") 
        strMatterId = request.GET.get("EF_MatterId", "") 
        strCount = request.GET.get("EF_MatterCount", "") 
        arrValidItems = PerchaseMatterDetails.objects.all() 

        if (strId != ""):
            arrValidItems = arrValidItems.filter(id__contains = int(strId))
        if (strFormId != ""):
            arrValidItems = arrValidItems.filter(EF_FormId = strFormId)
        if (strMatterId != "" and strMatterId != "0"):
            arrValidItems = arrValidItems.filter(EF_MatterId__contains = strMatterId)
        if (strCount != ""):
            arrValidItems = arrValidItems.filter(EF_MatterCount__contains = strCount)

        return HttpResponse(self.to_json(arrValidItems), content_type = 'application/json', status = 200)

    def post(self, request):
        strFormId = request.POST.get("EF_FormId", "") 
        strMatterId = request.POST.get("EF_MatterId", "") 
        strCount = request.POST.get("EF_MatterCount", "") 

        newItem = PerchaseMatterDetails.objects.create(EF_FormId = strFormId, EF_MatterId = strMatterId,
                EF_MatterCount = strCount)

        jsonDict = {}
        jsonDict["id"] = newItem.id
        jsonDict["EF_FormId"] = int(strFormId)
        jsonDict["EF_MatterId"] = int(strMatterId)
        jsonDict["EF_MatterCount"] = int(strCount)
        jsonStr = json.dumps(jsonDict, ensure_ascii=True) 

        return JsonResponse(jsonStr, status = 201, safe=False)

    def put(self, request):
        intCurId = int(request.PUT.get("id"))
        curItem = PerchaseMatterDetails.objects.get(id = intCurId)
        curItem.EF_FormId = int(request.PUT.get("EF_FormId"))
        curItem.EF_MatterId= request.PUT.get("EF_MatterId", "")
        curItem.EF_MatterCount= request.PUT.get("EF_MatterCount", "")
        curItem.save()

        jsonDict = {}
        jsonDict["id"] = curItem.id
        jsonDict["EF_FormId"] = int(curItem.EF_FormId)
        jsonDict["EF_MatterId"] = int(curItem.EF_MatterId)
        jsonDict["EF_MatterCount"] = int(curItem.EF_MatterCount)
        jsonStr = json.dumps(jsonDict, ensure_ascii=True) 

        return JsonResponse(jsonStr, status = 200, safe=False)

    def delete(self, request, intTypeId):
        curItem = PrePerchaseMatterDetails.objects.get(id = int(intTypeId))
        curItem.delete()
        return HttpResponse(status = 200)

    def to_json(self, objects):
        return serializers.serialize('json', objects)


#预采购清单
class CPerchaseFormsView(Resource):

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

        arrValidItems = PerchaseForms.objects.all() 

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
        curItem = PerchaseForms.objects.get(id = int(intTypeId))
        
        #删除相对应的药品明细
        subItemList = PerchaseMatterDetails.objects.all().filter(EF_FormId = intTypeId)
        for index in subItemList:
            index.delete()

        curItem.delete()
        return HttpResponse(status = 200)

    def to_json(self, objects):
        return serializers.serialize('json', objects)


#入库操作
class CImportMatterDetailsView(Resource):

    def get(self, request):
        strId = request.GET.get("id", "") 
        strFormId = request.GET.get("EF_FormId", "") 
        strMatterId = request.GET.get("EF_MatterId", "") 
        strCount = request.GET.get("EF_MatterCount", "") 
        arrValidItems = ImportMatterDetails.objects.all() 

        if (strId != ""):
            arrValidItems = arrValidItems.filter(id__contains = int(strId))
        if (strFormId != ""):
            arrValidItems = arrValidItems.filter(EF_FormId = strFormId)
        if (strMatterId != "" and strMatterId != "0"):
            arrValidItems = arrValidItems.filter(EF_MatterId__contains = strMatterId)
        if (strCount != ""):
            arrValidItems = arrValidItems.filter(EF_MatterCount__contains = strCount)

        return HttpResponse(self.to_json(arrValidItems), content_type = 'application/json', status = 200)

    def post(self, request):
        strFormId = request.POST.get("EF_FormId", "") 
        strMatterId = request.POST.get("EF_MatterId", "") 
        strCount = request.POST.get("EF_MatterCount", "") 

        newItem = ImportMatterDetails.objects.create(EF_FormId = strFormId, EF_MatterId = strMatterId,
                EF_MatterCount = strCount)

        jsonDict = {}
        jsonDict["id"] = newItem.id
        jsonDict["EF_FormId"] = int(strFormId)
        jsonDict["EF_MatterId"] = int(strMatterId)
        jsonDict["EF_MatterCount"] = int(strCount)
        jsonStr = json.dumps(jsonDict, ensure_ascii=True) 

        return JsonResponse(jsonStr, status = 201, safe=False)

    def put(self, request):
        intCurId = int(request.PUT.get("id"))
        curItem = ImportMatterDetails.objects.get(id = intCurId)
        curItem.EF_FormId = int(request.PUT.get("EF_FormId"))
        curItem.EF_MatterId= request.PUT.get("EF_MatterId", "")
        curItem.EF_MatterCount= request.PUT.get("EF_MatterCount", "")
        curItem.save()

        jsonDict = {}
        jsonDict["id"] = curItem.id
        jsonDict["EF_FormId"] = int(curItem.EF_FormId)
        jsonDict["EF_MatterId"] = int(curItem.EF_MatterId)
        jsonDict["EF_MatterCount"] = int(curItem.EF_MatterCount)
        jsonStr = json.dumps(jsonDict, ensure_ascii=True) 

        return JsonResponse(jsonStr, status = 200, safe=False)

    def delete(self, request, intTypeId):
        curItem = ImportMatterDetails.objects.get(id = int(intTypeId))
        curItem.delete()
        return HttpResponse(status = 200)

    def to_json(self, objects):
        return serializers.serialize('json', objects)


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
        subItemList = ImportMatterDetails.objects.all().filter(EF_FormId = intTypeId)
        for index in subItemList:
            index.delete()

        curItem.delete()
        return HttpResponse(status = 200)

    def to_json(self, objects):
        return serializers.serialize('json', objects)


#预约操作
class CReserveMatterDetailsView(Resource):

    def get(self, request):
        strId = request.GET.get("id", "") 
        strFormId = request.GET.get("EF_FormId", "") 
        strMatterId = request.GET.get("EF_MatterId", "") 
        strCount = request.GET.get("EF_MatterCount", "") 
        arrValidItems = ReserveMatterDetails.objects.all() 

        if (strId != ""):
            arrValidItems = arrValidItems.filter(id__contains = int(strId))
        if (strFormId != ""):
            arrValidItems = arrValidItems.filter(EF_FormId = strFormId)
        if (strMatterId != "" and strMatterId != "0"):
            arrValidItems = arrValidItems.filter(EF_MatterId__contains = strMatterId)
        if (strCount != ""):
            arrValidItems = arrValidItems.filter(EF_MatterCount__contains = strCount)

        return HttpResponse(self.to_json(arrValidItems), content_type = 'application/json', status = 200)

    def post(self, request):
        strFormId = request.POST.get("EF_FormId", "") 
        strMatterId = request.POST.get("EF_MatterId", "") 
        strCount = request.POST.get("EF_MatterCount", "") 

        newItem = ReserveMatterDetails.objects.create(EF_FormId = strFormId, EF_MatterId = strMatterId,
                EF_MatterCount = strCount)

        jsonDict = {}
        jsonDict["id"] = newItem.id
        jsonDict["EF_FormId"] = int(strFormId)
        jsonDict["EF_MatterId"] = int(strMatterId)
        jsonDict["EF_MatterCount"] = int(strCount)
        jsonStr = json.dumps(jsonDict, ensure_ascii=True) 

        return JsonResponse(jsonStr, status = 201, safe=False)

    def put(self, request):
        intCurId = int(request.PUT.get("id"))
        curItem = ReserveMatterDetails.objects.get(id = intCurId)
        curItem.EF_FormId = int(request.PUT.get("EF_FormId"))
        curItem.EF_MatterId= request.PUT.get("EF_MatterId", "")
        curItem.EF_MatterCount= request.PUT.get("EF_MatterCount", "")
        curItem.save()

        jsonDict = {}
        jsonDict["id"] = curItem.id
        jsonDict["EF_FormId"] = int(curItem.EF_FormId)
        jsonDict["EF_MatterId"] = int(curItem.EF_MatterId)
        jsonDict["EF_MatterCount"] = int(curItem.EF_MatterCount)
        jsonStr = json.dumps(jsonDict, ensure_ascii=True) 

        return JsonResponse(jsonStr, status = 200, safe=False)

    def delete(self, request, intTypeId):
        curItem = ReserveMatterDetails.objects.get(id = int(intTypeId))
        curItem.delete()
        return HttpResponse(status = 200)

    def to_json(self, objects):
        return serializers.serialize('json', objects)


#预约清单
class CReserveFormsView(Resource):

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

        arrValidItems = ReserveForms.objects.all() 

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
        curItem = ReserveForms.objects.get(id = int(intTypeId))
        
        #删除相对应的药品明细
        subItemList = ReserveMatterDetails.objects.all().filter(EF_FormId = intTypeId)
        for index in subItemList:
            index.delete()

        curItem.delete()
        return HttpResponse(status = 200)

    def to_json(self, objects):
        return serializers.serialize('json', objects)


#出库操作
class CExportMatterDetailsView(Resource):

    def get(self, request):
        strId = request.GET.get("id", "") 
        strFormId = request.GET.get("EF_FormId", "") 
        strMatterId = request.GET.get("EF_MatterId", "") 
        strCount = request.GET.get("EF_MatterCount", "") 
        arrValidItems = ExportMatterDetails.objects.all() 

        if (strId != ""):
            arrValidItems = arrValidItems.filter(id__contains = int(strId))
        if (strFormId != ""):
            arrValidItems = arrValidItems.filter(EF_FormId = strFormId)
        if (strMatterId != "" and strMatterId != "0"):
            arrValidItems = arrValidItems.filter(EF_MatterId__contains = strMatterId)
        if (strCount != ""):
            arrValidItems = arrValidItems.filter(EF_MatterCount__contains = strCount)

        return HttpResponse(self.to_json(arrValidItems), content_type = 'application/json', status = 200)

    def post(self, request):
        strFormId = request.POST.get("EF_FormId", "") 
        strMatterId = request.POST.get("EF_MatterId", "") 
        strCount = request.POST.get("EF_MatterCount", "") 

        newItem = ExportMatterDetails.objects.create(EF_FormId = strFormId, EF_MatterId = strMatterId,
                EF_MatterCount = strCount)

        jsonDict = {}
        jsonDict["id"] = newItem.id
        jsonDict["EF_FormId"] = int(strFormId)
        jsonDict["EF_MatterId"] = int(strMatterId)
        jsonDict["EF_MatterCount"] = int(strCount)
        jsonStr = json.dumps(jsonDict, ensure_ascii=True) 

        return JsonResponse(jsonStr, status = 201, safe=False)

    def put(self, request):
        intCurId = int(request.PUT.get("id"))
        curItem = ExportMatterDetails.objects.get(id = intCurId)
        curItem.EF_FormId = int(request.PUT.get("EF_FormId"))
        curItem.EF_MatterId= request.PUT.get("EF_MatterId", "")
        curItem.EF_MatterCount= request.PUT.get("EF_MatterCount", "")
        curItem.save()

        jsonDict = {}
        jsonDict["id"] = curItem.id
        jsonDict["EF_FormId"] = int(curItem.EF_FormId)
        jsonDict["EF_MatterId"] = int(curItem.EF_MatterId)
        jsonDict["EF_MatterCount"] = int(curItem.EF_MatterCount)
        jsonStr = json.dumps(jsonDict, ensure_ascii=True) 

        return JsonResponse(jsonStr, status = 200, safe=False)

    def delete(self, request, intTypeId):
        curItem = ExportMatterDetails.objects.get(id = int(intTypeId))
        curItem.delete()
        return HttpResponse(status = 200)

    def to_json(self, objects):
        return serializers.serialize('json', objects)

#出库清单
class CExportFormsView(Resource):

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

        arrValidItems = ExportForms.objects.all() 

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
        curItem = ExportForms.objects.get(id = int(intTypeId))
        
        #删除相对应的药品明细
        subItemList = ExportMatterDetails.objects.all().filter(EF_FormId = intTypeId)
        for index in subItemList:
            index.delete()

        curItem.delete()
        return HttpResponse(status = 200)

    def to_json(self, objects):
        return serializers.serialize('json', objects)



