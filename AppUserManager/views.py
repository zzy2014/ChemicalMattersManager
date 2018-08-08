from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from simple_rest import Resource #第三方的小类
from django.core import serializers #导入序列化
from .models import UserTypes, UserStates
from .models import SuperAdministrators, Administrators, ChiefCollegeLeaders, CollegeLeaders
from .models import Teachers, Finances, StudentTypes, Students
import json

#登录检测入口
def loginVerify(request):

    intUserId = -1 #返回的用户ID，且作为结果码，-1表示访问出错,0表示用户名或密码错误，>0表示登录正常
    strUserType ="none"
    strUserSubType ="none"
    bIsContinue = True

    if request.method == 'GET' :
        intUserId = 0
        strUserName = request.GET.get('name')
        strPassWord = request.GET.get('password')

        #是否为超级管理员
        if bIsContinue:
            setSuperAdmin = SuperAdministrators.objects.filter(EF_UserName=strUserName, EF_PassWord=strPassWord)
            if (setSuperAdmin.count() > 0):
                bIsContinue = False
                strUserType = "SuperAdmin"
                intUserId = setSuperAdmin[0].id

        #是否为管理员
        if bIsContinue:
            setAdmin = Administrators.objects.filter(EF_UserName=strUserName, EF_PassWord=strPassWord)
            if (setAdmin.count() > 0):
                bIsContinue = False
                strUserType = "Admin"
                intUserId = setAdmin[0].id


       #是否为院长
        if bIsContinue:
            setChiefLeaders = ChiefCollegeLeaders.objects.filter(EF_UserName=strUserName, EF_PassWord=strPassWord)
            if (setChiefLeaders.count() > 0):
                bIsContinue = False
                strUserType = "ChiefLeader"
                intUserId = setChiefLeaders[0].id

        #是否为副院长
        if bIsContinue:
            setLeaders = CollegeLeaders.objects.filter(EF_UserName=strUserName, EF_PassWord=strPassWord)
            if (setLeaders.count() > 0):
                bIsContinue = False
                strUserType = "Leader"
                intUserId = setLeaders[0].id

        #是否为老师
        if bIsContinue:
            setTeachers = Teachers.objects.filter(EF_UserName=strUserName, EF_PassWord=strPassWord)
            if (setTeachers.count() > 0):
                bIsContinue = False
                strUserType = "Teacher"
                intUserId = setTeachers[0].id

        #是否为学生
        if bIsContinue:
            setStudents = Students.objects.filter(EF_UserName=strUserName, EF_PassWord=strPassWord)
            if (setStudents.count() > 0):
                bIsContinue = False
                strUserType = "Student"
                strUserSubType = "Bacholer"
                intUserId = setStudents[0].id


    return JsonResponse({'userId':intUserId, 'userType':strUserType, 'userSubType':strUserSubType})


#用户登录成功后界面接口，用以为每种用户分配主页
def userHome(request):
    if (request.method != 'GET'):
        return HttpResponse("访问错误");
    else:
        intUserId = request.GET.get('userId')
        strUserType = request.GET.get('userType')
        strUserSubType = request.GET.get('userSubType')

        if (strUserType == "SuperAdmin"):
            return render(request, 'userHome.html')

        elif (strUserType == "Admin"):
            return HttpResponse(strUserType)
        elif (strUserType == "ChiefLeader"):
            return HttpResponse(strUserType)
        elif (strUserType == "Leader"):
            return HttpResponse(strUserType)
        elif (strUserType == "Teacher"):
            return HttpResponse(strUserType)
        elif (strUserType == "Student"):
            return HttpResponse(strUserType)

    return HttpResponse(strUserType)


#用户状态接口
class CUserStatesView(Resource):

    def get(self, request):
        strId = request.GET.get("id", "") 
        strTypeName = request.GET.get("EF_TypeName", "") 
        arrAllTypes = UserStates.objects.all()
        arrValidTypes = arrAllTypes 

        if (strId != ""):
            arrValidTypes = arrValidTypes.filter(id__contains = int(strId))
        if (strTypeName != ""):
            arrValidTypes = arrValidTypes.filter(EF_TypeName__contains = strTypeName)

        return HttpResponse(self.to_json(arrValidTypes), content_type = 'application/json', status = 200)

    def post(self, request):
        strTypeName = request.POST.get("EF_TypeName", "")
        newItem = UserStates.objects.create(EF_TypeName = strTypeName)
        return JsonResponse({"id":newItem.id,"EF_TypeName":newItem.EF_TypeName}, status = 201)

    def put(self, request):
        intCurId = int(request.PUT.get("id"))
        curUserType = UserStates.objects.get(id = intCurId)
        curUserType.EF_TypeName= request.PUT.get("EF_TypeName", "")
        curUserType.save()
        return JsonResponse({"id":curUserType.id, "EF_TypeName":curUserType.EF_TypeName}, status = 200)

    def delete(self, request, intTypeId):
        curUserType = UserStates.objects.get(id = int(intTypeId))
        curUserType.delete()
        return HttpResponse(status = 200)

    def to_json(self, objects):
        return serializers.serialize('json', objects)


#用户类型接口
class CUserTypesView(Resource):

    def get(self, request):
        strId = request.GET.get("id", "") 
        strTypeName = request.GET.get("EF_TypeName", "") 
        arrAllTypes = UserTypes.objects.all()
        arrValidTypes = arrAllTypes 

        if (strId != ""):
            arrValidTypes = arrValidTypes.filter(id__contains = int(strId))
        if (strTypeName != ""):
            arrValidTypes = arrValidTypes.filter(EF_TypeName__contains = strTypeName)

        return HttpResponse(self.to_json(arrValidTypes), content_type = 'application/json', status = 200)

    def post(self, request):
        strTypeName = request.POST.get("EF_TypeName", "")
        newItem = UserTypes.objects.create(EF_TypeName = strTypeName)
        return JsonResponse({"id":newItem.id,"EF_TypeName":newItem.EF_TypeName}, status = 201)

    def put(self, request):
        intCurId = int(request.PUT.get("id"))
        curUserType = UserTypes.objects.get(id = intCurId)
        curUserType.EF_TypeName= request.PUT.get("EF_TypeName", "")
        curUserType.save()
        return JsonResponse({"id":curUserType.id, "EF_TypeName":curUserType.EF_TypeName}, status = 200)

    def delete(self, request, intTypeId):
        curUserType = UserTypes.objects.get(id = int(intTypeId))
        curUserType.delete()
        return HttpResponse(status = 200)

    def to_json(self, objects):
        return serializers.serialize('json', objects)

#学生类型接口
class CStudentTypesView(Resource):

    def get(self, request):
        strId = request.GET.get("id", "") 
        strTypeName = request.GET.get("EF_TypeName", "") 
        arrAllTypes = StudentTypes.objects.all()
        arrValidTypes = arrAllTypes 

        if (strId != ""):
            arrValidTypes = arrValidTypes.filter(id__contains = int(strId))
        if (strTypeName != ""):
            arrValidTypes = arrValidTypes.filter(EF_TypeName__contains = strTypeName)

        return HttpResponse(self.to_json(arrValidTypes), content_type = 'application/json', status = 200)

    def post(self, request):
        strTypeName = request.POST.get("EF_TypeName", "")
        newItem = StudentTypes.objects.create(EF_TypeName = strTypeName)
        return JsonResponse({"id":newItem.id,"EF_TypeName":newItem.EF_TypeName}, status = 201)

    def put(self, request):
        intCurId = int(request.PUT.get("id"))
        curUserType = StudentTypes.objects.get(id = intCurId)
        curUserType.EF_TypeName= request.PUT.get("EF_TypeName", "")
        curUserType.save()
        return JsonResponse({"id":curUserType.id, "EF_TypeName":curUserType.EF_TypeName}, status = 200)

    def delete(self, request, intTypeId):
        curUserType = StudentTypes.objects.get(id = int(intTypeId))
        curUserType.delete()
        return HttpResponse(status = 200)

    def to_json(self, objects):
        return serializers.serialize('json', objects)

#管理员接口
class CAdministratorsView(Resource):

    def get(self, request):
        strId = request.GET.get("id", "") 
        strUserStateId = request.GET.get("EF_UserStateId", "") 
        strUserName = request.GET.get("EF_UserName", "") 
        strPassWord = request.GET.get("EF_PassWord", "") 
        strOfficeAddress = request.GET.get("EF_OfficeAddress", "") 
        strPhoneNum = request.GET.get("EF_PhoneNum", "") 
        arrAllItems = Administrators.objects.all()
        arrValidItems = arrAllItems

        if (strId != ""):
            arrValidItems = arrValidItems.filter(id__contains = int(strId))
        if (strUserStateId != "" and strUserStateId != "0"):
            arrValidItems = arrValidItems.filter(EF_UserStateId__contains = int(strUserStateId))
        if (strUserName != ""):
            arrValidItems = arrValidItems.filter(EF_UserName__contains = strUserName)
        if (strPassWord != ""):
            arrValidItems = arrValidItems.filter(EF_PassWord__contains = strPassWord)
        if (strOfficeAddress != ""):
            arrValidItems = arrValidItems.filter(EF_OfficeAddress__contains = strOfficeAddress)
        if (strPhoneNum != ""):
            arrValidItems = arrValidItems.filter(EF_PhoneNum__contains = strPhoneNum)

        return HttpResponse(self.to_json(arrValidItems), content_type = 'application/json', status = 200)

    def post(self, request):
        strStateId = request.POST.get("EF_UserStateId", "0") 
        strUserName = request.POST.get("EF_UserName", "") 
        strPassWord = request.POST.get("EF_PassWord", "") 
        strOfficeAddress = request.POST.get("EF_OfficeAddress", "") 
        strPhoneNum = request.POST.get("EF_PhoneNum", "") 
        newItem = Administrators.objects.create(EF_UserStateId = int(strStateId), EF_UserName = strUserName,
                EF_PassWord = strPassWord, EF_OfficeAddress = strOfficeAddress, EF_PhoneNum = strPhoneNum)

        jsonDict = {}
        jsonDict["id"] = newItem.id
        jsonDict["EF_UserStateId"] = int(strStateId)
        jsonDict["EF_UserName"] = strUserName
        jsonDict["EF_PassWord"] = strPassWord
        jsonDict["EF_OfficeAddress"] = strOfficeAddress
        jsonDict["EF_PhoneNum"] = strPhoneNum

        jsonStr = json.dumps(jsonDict, ensure_ascii=False) 

        return JsonResponse(jsonStr, status = 201, safe=False)

    def put(self, request):
        intCurId = int(request.PUT.get("id"))
        strStateId = request.PUT.get("EF_UserStateId", "0") 
        strUserName = request.PUT.get("EF_UserName", "") 
        strPassWord = request.PUT.get("EF_PassWord", "") 
        strOfficeAddress = request.PUT.get("EF_OfficeAddress", "") 
        strPhoneNum = request.PUT.get("EF_PhoneNum", "") 

        curAdmin = Administrators.objects.get(id = intCurId)
        curAdmin.EF_UserStateId = strStateId
        curAdmin.EF_UserName = strUserName
        curAdmin.EF_PassWord = strPassWord
        curAdmin.EF_OfficeAddress = strOfficeAddress
        curAdmin.EF_PhoneNum = strPhoneNum
        curAdmin.save()

        jsonDict = {}
        jsonDict["id"] = intCurId 
        jsonDict["EF_UserStateId"] = strStateId
        jsonDict["EF_UserName"] = strUserName
        jsonDict["EF_PassWord"] = strPassWord
        jsonDict["EF_OfficeAddress"] = strOfficeAddress
        jsonDict["EF_PhoneNum"] = strPhoneNum

        jsonStr = json.dumps(jsonDict, ensure_ascii=False) 

        return JsonResponse(jsonStr, status = 200, safe = False)

    def delete(self, request, intTypeId):
        curAdmin = Administrators.objects.get(id = int(intTypeId))
        curAdmin.delete()
        return HttpResponse(status = 200)

    def to_json(self, objects):
        return serializers.serialize('json', objects)

#院长接口
class CChiefCollegeLeadersView(Resource):

    def get(self, request):
        strId = request.GET.get("id", "") 
        strUserStateId = request.GET.get("EF_UserStateId", "") 
        strTeacherId = request.GET.get("EF_TeacherId", "") 
        strUserName = request.GET.get("EF_UserName", "") 
        strPassWord = request.GET.get("EF_PassWord", "") 
        strOfficeAddress = request.GET.get("EF_OfficeAddress", "") 
        strPhoneNum = request.GET.get("EF_PhoneNum", "") 
        arrAllItems = ChiefCollegeLeaders.objects.all()
        arrValidItems = arrAllItems

        if (strId != ""):
            arrValidItems = arrValidItems.filter(id__contains = int(strId))
        if (strUserStateId != "" and strUserStateId != "0"):
            arrValidItems = arrValidItems.filter(EF_UserStateId__contains = int(strUserStateId))
        if (strTeacherId != "" and strTeacherId != "0"):
            arrValidItems = arrValidItems.filter(EF_TeacherId_contains = int(strTeacherId))
        if (strUserName != ""):
            arrValidItems = arrValidItems.filter(EF_UserName__contains = strUserName)
        if (strPassWord != ""):
            arrValidItems = arrValidItems.filter(EF_PassWord__contains = strPassWord)
        if (strOfficeAddress != ""):
            arrValidItems = arrValidItems.filter(EF_OfficeAddress__contains = strOfficeAddress)
        if (strPhoneNum != ""):
            arrValidItems = arrValidItems.filter(EF_PhoneNum__contains = strPhoneNum)

        return HttpResponse(self.to_json(arrValidItems), content_type = 'application/json', status = 200)

    def post(self, request):
        strStateId = request.POST.get("EF_UserStateId", "0") 
        strTeacherId = request.POST.get("EF_TeacherId", "0") 
        strUserName = request.POST.get("EF_UserName", "") 
        strPassWord = request.POST.get("EF_PassWord", "") 
        strOfficeAddress = request.POST.get("EF_OfficeAddress", "") 
        strPhoneNum = request.POST.get("EF_PhoneNum", "") 
        newItem = ChiefCollegeLeaders.objects.create(EF_UserStateId = int(strStateId), EF_TeacherId = int(strTeacherId),
            EF_UserName = strUserName,EF_PassWord = strPassWord, EF_OfficeAddress = strOfficeAddress, EF_PhoneNum = strPhoneNum)

        jsonDict = {}
        jsonDict["id"] = newItem.id
        jsonDict["EF_UserStateId"] = int(strStateId)
        jsonDict["EF_TeacherId"] = int(strTeacherId)
        jsonDict["EF_UserName"] = strUserName
        jsonDict["EF_PassWord"] = strPassWord
        jsonDict["EF_OfficeAddress"] = strOfficeAddress
        jsonDict["EF_PhoneNum"] = strPhoneNum

        jsonStr = json.dumps(jsonDict, ensure_ascii=False) 

        return JsonResponse(jsonStr, status = 201, safe=False)

    def put(self, request):
        intCurId = int(request.PUT.get("id"))
        strStateId = request.PUT.get("EF_UserStateId", "0") 
        strTeacherId = request.PUT.get("EF_TeacherId", "0") 
        strUserName = request.PUT.get("EF_UserName", "") 
        strPassWord = request.PUT.get("EF_PassWord", "") 
        strOfficeAddress = request.PUT.get("EF_OfficeAddress", "") 
        strPhoneNum = request.PUT.get("EF_PhoneNum", "") 

        curAdmin = ChiefCollegeLeaders.objects.get(id = intCurId)
        curAdmin.EF_UserStateId = int(strStateId)
        curAdmin.EF_TeacherId = int(strTeacherId)
        curAdmin.EF_UserName = strUserName
        curAdmin.EF_PassWord = strPassWord
        curAdmin.EF_OfficeAddress = strOfficeAddress
        curAdmin.EF_PhoneNum = strPhoneNum
        curAdmin.save()

        jsonDict = {}
        jsonDict["id"] = intCurId 
        jsonDict["EF_UserStateId"] = strStateId
        jsonDict["EF_TeacherId"] = strTeacherId
        jsonDict["EF_UserName"] = strUserName
        jsonDict["EF_PassWord"] = strPassWord
        jsonDict["EF_OfficeAddress"] = strOfficeAddress
        jsonDict["EF_PhoneNum"] = strPhoneNum

        jsonStr = json.dumps(jsonDict, ensure_ascii=False) 

        return JsonResponse(jsonStr, status = 200, safe = False)

    def delete(self, request, intTypeId):
        curAdmin = ChiefCollegeLeaders.objects.get(id = int(intTypeId))
        curAdmin.delete()
        return HttpResponse(status = 200)

    def to_json(self, objects):
        return serializers.serialize('json', objects)
