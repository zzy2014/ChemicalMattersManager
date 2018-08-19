from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from simple_rest import Resource #第三方的小类
from django.core import serializers #导入序列化
from django.core.files.base import ContentFile
from .models import UserTypes, UserStates
from .models import SuperAdministrators, Administrators, ChiefCollegeLeaders, CollegeLeaders
from .models import Teachers, Finances, StudentTypes, Students
import json


#注册入口
def register(request):
    intRetCode = -1 #返回结果码，小于0表示注册失败，=0表示当前用户名己存在，>0表示注册成功
    strUserType = "";
    strUserName = ""
    strPassWord = "";

    if request.method == 'POST' :
        strUserType = request.POST.get('type')
        strUserName = request.POST.get('name')
        strPassWord = request.POST.get('password')

    #有空值时返回
    if (strUserType == "" or strUserName == "" or strPassWord == ""):
         return JsonResponse({'userId':intUserId})

    #拆分后若不足两项，返回
    arrTypeIndex = strUserType.split("_");
    if (len(arrTypeIndex) < 3):
         return JsonResponse({'userId':intUserId})

    if (arrTypeIndex[0] == "User"):
        #是否为管理员
        if (arrTypeIndex[2] == Administrators.Type):
            setAdmin = Administrators.objects.filter(EF_UserName = strUserName)
            if (setAdmin.count() > 0):
                intRetCode = 0
            else:
                newItem = Administrators.objects.create(EF_UserStateId = 0, EF_UserName = strUserName,
                    EF_PassWord = strPassWord, EF_OfficeAddress = "", EF_PhoneNum = "")

                intRetCode = newItem.id
            
        #是否为院长
        elif (arrTypeIndex[2] == ChiefCollegeLeaders.Type):
            setChiefLeaders = ChiefCollegeLeaders.objects.filter(EF_UserName=strUserName)
            if (setChiefLeaders.count() > 0):
                intRetCode = 0
            else:
                newItem = ChiefCollegeLeaders.objects.create(EF_UserStateId = 0, EF_TeacherId = 0, EF_UserName = strUserName,
                     EF_PassWord = strPassWord, EF_OfficeAddress = "", EF_PhoneNum = "")

                intRetCode = newItem.id

        #是否为副院长
        elif (arrTypeIndex[2] == CollegeLeaders.Type):
            setLeaders = CollegeLeaders.objects.filter(EF_UserName=strUserName)
            if (setLeaders.count() > 0):
                intRetCode = 0
            else:
                newItem = CollegeLeaders.objects.create(EF_UserStateId = 0, EF_TeacherId = 0,
                     EF_UserName = strUserName, EF_PassWord = strPassWord, EF_OfficeAddress = "", EF_PhoneNum = "")

                intRetCode = newItem.id

        #是否为老师
        elif (arrTypeIndex[2] == Teachers.Type):
            setTeachers = Teachers.objects.filter(EF_UserName=strUserName)
            if (setTeachers.count() > 0):
                intRetCode = 0
            else:
                newItem = Teachers.objects.create(EF_UserStateId = 0, EF_UserName = strUserName,
                   EF_PassWord = strPassWord, EF_OfficeAddress = "", EF_PhoneNum = "")

                intRetCode = newItem.id

    if (arrTypeIndex[0] == "Student"):
        setStudent = Students.objects.filter(EF_UserName=strUserName, EF_TypeId = int(arrTypeIndex[1]))
        if (setStudent.count() > 0):
            intRetCode = 0
        else:
            newItem = Students.objects.create(EF_UserStateId = 0, EF_TypeId = int(arrTypeIndex[1]),
                EF_TeacherId = 0, EF_UserName = strUserName, EF_PassWord = strPassWord)

            intRetCode = newItem.id

    return JsonResponse({'retCode':intRetCode})


#登录检测入口
def loginVerify(request):

    intUserId = -1 #返回的用户ID，且作为结果码，小于0表示用户名或密码错误，>0表示登录正常
    strUserType = "";
    strUserName = ""
    strPassWord = "";

    if request.method == 'POST' :
        strUserType = request.POST.get('type')
        strUserName = request.POST.get('name')
        strPassWord = request.POST.get('password')

    if (strUserType == "" or strUserName == "" or strPassWord == ""):
         return JsonResponse({'userId':intUserId})

    #拆分后若不足两项，返回
    arrTypeIndex = strUserType.split("_");
    if (len(arrTypeIndex) < 3):
         return JsonResponse({'userId':intUserId})


    if (arrTypeIndex[0] == "User"):
        #是否为超级管理员
        if (arrTypeIndex[2] == SuperAdministrators.Type):
            setSuperAdmin = SuperAdministrators.objects.filter(EF_UserName=strUserName, EF_PassWord=strPassWord)
            if (setSuperAdmin.count() > 0):
                intUserId = setSuperAdmin[0].id

        #是否为管理员
        elif (arrTypeIndex[2] == Administrators.Type):
            setAdmin = Administrators.objects.filter(EF_UserName=strUserName, EF_PassWord=strPassWord)
            if (setAdmin.count() > 0):
                intUserId = setAdmin[0].id

        #是否为院长
        elif (arrTypeIndex[2] == ChiefCollegeLeaders.Type):
            setChiefLeaders = ChiefCollegeLeaders.objects.filter(EF_UserName=strUserName, EF_PassWord=strPassWord)
            if (setChiefLeaders.count() > 0):
                intUserId = setChiefLeaders[0].id

        #是否为副院长
        elif (arrTypeIndex[2] == CollegeLeaders.Type):
            setLeaders = CollegeLeaders.objects.filter(EF_UserName=strUserName, EF_PassWord=strPassWord)
            if (setLeaders.count() > 0):
                intUserId = setLeaders[0].id

        #是否为老师
        elif (arrTypeIndex[2] == Teachers.Type):
            setTeachers = Teachers.objects.filter(EF_UserName=strUserName, EF_PassWord=strPassWord)
            if (setTeachers.count() > 0):
                intUserId = setTeachers[0].id

    #是否为学生
    if (arrTypeIndex[0] == "Student"):
        setStudent = Students.objects.filter(EF_UserName=strUserName, EF_PassWord = strPassWord, EF_TypeId = int(arrTypeIndex[1]))
        if (setStudent.count() > 0):
            intUserId = setStudent[0].id

    return JsonResponse({'userId':intUserId})


#用户登录成功后界面接口，用以为每种用户分配主页
def userHome(request):
    if (request.method != 'GET'):
        return HttpResponse("访问错误");

    intUserId = request.GET.get('userId')
    strUserType = request.GET.get('userType')
    strUserName = ""
    strUserPassWord = request.GET.get('userPassWord')

    #拆分后若不足两项，返回
    arrTypeIndex = strUserType.split("_");
    if (len(arrTypeIndex) < 3):
         return JsonResponse({'userId':intUserId})

    #按用户的类别加载不同的个人界面
    if (arrTypeIndex[0] == "User"):
        if (arrTypeIndex[2] == SuperAdministrators.Type):
            setSuperAdmin = SuperAdministrators.objects.filter(id = intUserId, EF_PassWord = strUserPassWord)
            if (setSuperAdmin.count() > 0):
                strUserName = setSuperAdmin[0].EF_UserName
        elif (arrTypeIndex[2] == Administrators.Type):
            setAdmin = Administrators.objects.filter(id = intUserId, EF_PassWord = strUserPassWord)
            if (setAdmin.count() > 0):
                strUserName = setAdmin[0].EF_UserName
        elif (arrTypeIndex[2] == ChiefCollegeLeaders.Type):
            setChiefLeader = ChiefCollegeLeaders.objects.filter(id = intUserId, EF_PassWord = strUserPassWord)
            if (setChiefLeader.count() > 0):
                strUserName = setChiefLeader[0].EF_UserName
        elif (arrTypeIndex[2] == CollegeLeaders.Type):
            setLeader = CollegeLeaders.objects.filter(id = intUserId, EF_PassWord = strUserPassWord)
            if (setLeader.count() > 0):
                strUserName = setLeader[0].EF_UserName
        elif (arrTypeIndex[2] == Teachers.Type):
            setTeacher = Teachers.objects.filter(id = intUserId, EF_PassWord = strUserPassWord)
            if (setTeacher.count() > 0):
                strUserName = setTeacher[0].EF_UserName
    elif (arrTypeIndex[0] == "Student"):
        setStudent = Students.objects.filter(id = intUserId, EF_PassWord = strUserPassWord, EF_TypeId = int(arrTypeIndex[1]))
        if (setStudent.count() > 0):
            strUserName = setStudent[0].EF_UserName

    #没有找到任何用户
    if (strUserName == ""):
        return HttpResponse("用户名或密码错误")


    #设置session
    request.session['id'] = intUserId
    request.session['userType'] = strUserType
    request.session.set_expiry(0)


    context = {} #一个字典对象
    context['userType'] = arrTypeIndex[2] #传入模板中的变量
    context['userName'] = strUserName #传入模板中的变量
    return render(request, 'userHome.html', context)


#上传当前用户的头像
def uploadCurUserImage(request):
    #从session中获取登录的用户id
    intUserId = request.session.get('id', default=0)
    strUserType = request.session.get('userType', default='')

    #拆分后若不足两项，返回
    arrTypeIndex = strUserType.split("_");
    if (int(intUserId) <= 0 or len(arrTypeIndex) < 3 or request.method != 'POST'):
        return JsonResponse({'intRetCode':-1, 'newUrl':""})

    strNewUrl = ""
    imageContent = ContentFile(request.FILES.get('uploadImage').read())

    #按用户的类别加载不同的个人界面
    if (arrTypeIndex[0] == "User"):
        if (arrTypeIndex[2] == SuperAdministrators.Type):
            setSuperAdmin = SuperAdministrators.objects.filter(id = intUserId)
            if (setSuperAdmin.count() > 0):
               setSuperAdmin[0].EF_Image.delete()
               setSuperAdmin[0].EF_Image.save(request.FILES.get('uploadImage').name, imageContent) 
               setSuperAdmin[0].save()
               strNewUrl = setSuperAdmin[0].EF_Image.url

        elif (arrTypeIndex[2] == Administrators.Type):
            setAdmin = Administrators.objects.filter(id = intUserId)
            if (setAdmin.count() > 0):
                setAdmin[0].EF_Image.delete()
                setAdmin[0].EF_Image.save(request.FILES.get('uploadImage').name, imageContent) 
                setAdmin[0].save()
                strNewUrl = setAdmin[0].EF_Image.url
        elif (arrTypeIndex[2] == ChiefCollegeLeaders.Type):
            setChiefLeader = ChiefCollegeLeaders.objects.filter(id = intUserId)
            if (setChiefLeader.count() > 0):
                setChiefLeader[0].EF_Image.delete()
                setChiefLeader[0].EF_Image.save(request.FILES.get('uploadImage').name, imageContent) 
                setChiefLeader[0].save()
                strNewUrl = setChiefLeader[0].EF_Image.url
        elif (arrTypeIndex[2] == CollegeLeaders.Type):
            setLeader = CollegeLeaders.objects.filter(id = intUserId)
            if (setLeader.count() > 0):
                setLeader[0].EF_Image.delete()
                setLeader[0].EF_Image.save(request.FILES.get('uploadImage').name, imageContent) 
                setLeader[0].save()
                strNewUrl = setLeader[0].EF_Image.url
        elif (arrTypeIndex[2] == Teachers.Type):
            setTeacher = Teachers.objects.filter(id = intUserId)
            if (setTeacher.count() > 0):
                setTeacher[0].EF_Image.delete()
                setTeacher[0].EF_Image.save(request.FILES.get('uploadImage').name, imageContent) 
                setTeacher[0].save()
                strNewUrl = setTeacher[0].EF_Image.url
    elif (arrTypeIndex[0] == "Student"):
        setStudent = Students.objects.filter(id = intUserId, EF_TypeId = int(arrTypeIndex[1]))
        if (setStudent.count() > 0):
            setStudent[0].EF_Image.delete()
            setStudent[0].EF_Image.save(request.FILES.get('uploadImage').name, imageContent) 
            setStudent[0].save()
            strNewUrl = setStudent[0].EF_Image.url

    return JsonResponse({'intRetCode':1, 'newUrl':strNewUrl})



#获取当前登录的用户相关的信息
def getCurUserInfo(request):
    #从session中获取登录的用户id
    intUserId = request.session.get('id', default=0)
    strUserType = request.session.get('userType', default='')

    #拆分后若不足两项，返回
    arrTypeIndex = strUserType.split("_");
    if (len(arrTypeIndex) < 3):
         return JsonResponse({'userId':intUserId})

    strUserType = arrTypeIndex[2]
    strUserState = ""
    strUserOffice = ""
    strUserPhone = ""
    strImageUrl = ""

    #按用户的类别加载不同的个人界面
    if (arrTypeIndex[0] == "User"):
        if (arrTypeIndex[2] == SuperAdministrators.Type):
            setSuperAdmin = SuperAdministrators.objects.filter(id = intUserId)
            if (setSuperAdmin.count() > 0):
                strUserOffice = setSuperAdmin[0].EF_OfficeAddress
                strUserPhone = setSuperAdmin[0].EF_PhoneNum
                strImageUrl = setSuperAdmin[0].EF_Image.url
                setState = UserStates.objects.filter(id = setSuperAdmin[0].EF_UserStateId)
                if (setState.count() > 0):
                    strUserState = setState[0].EF_TypeName 

        elif (arrTypeIndex[2] == Administrators.Type):
            setAdmin = Administrators.objects.filter(id = intUserId)
            if (setAdmin.count() > 0):
                strUserOffice = setAdmin[0].EF_OfficeAddress
                strUserPhone = setAdmin[0].EF_PhoneNum
                strImageUrl = setAdmin[0].EF_Image.url
                setState = UserStates.objects.filter(id = setAdmin[0].EF_UserStateId)
                if (setState.count() > 0):
                    strUserState = setState[0].EF_TypeName 
        elif (arrTypeIndex[2] == ChiefCollegeLeaders.Type):
            setChiefLeader = ChiefCollegeLeaders.objects.filter(id = intUserId)
            if (setChiefLeader.count() > 0):
                strUserOffice = setChiefLeader[0].EF_OfficeAddress
                strUserPhone = setChiefLeader[0].EF_PhoneNum
                strImageUrl = setChiefLeader[0].EF_Image.url
                setState = UserStates.objects.filter(id = setChiefLeader[0].EF_UserStateId)
                if (setState.count() > 0):
                    strUserState = setState[0].EF_TypeName 
        elif (arrTypeIndex[2] == CollegeLeaders.Type):
            setLeader = CollegeLeaders.objects.filter(id = intUserId)
            if (setLeader.count() > 0):
                strUserOffice = setLeader[0].EF_OfficeAddress
                strUserPhone = setLeader[0].EF_PhoneNum
                strImageUrl = setLeader[0].EF_Image.url
                setState = UserStates.objects.filter(id = setLeader[0].EF_UserStateId)
                if (setState.count() > 0):
                    strUserState = setState[0].EF_TypeName 
        elif (arrTypeIndex[2] == Teachers.Type):
            setTeacher = Teachers.objects.filter(id = intUserId)
            if (setTeacher.count() > 0):
                strUserOffice = setTeacher[0].EF_OfficeAddress
                strUserPhone = setTeacher[0].EF_PhoneNum
                strImageUrl = setTeacher[0].EF_Image.url
                setState = UserStates.objects.filter(id = setTeacher[0].EF_UserStateId)
                if (setState.count() > 0):
                    strUserState = setState[0].EF_TypeName 
    elif (arrTypeIndex[0] == "Student"):
        setStudent = Students.objects.filter(id = intUserId, EF_TypeId = int(arrTypeIndex[1]))
        if (setStudent.count() > 0):
            strUserOffice = setStudent[0].EF_OfficeAddress
            strUserPhone = setStudent[0].EF_PhoneNum
            strImageUrl = setStudent[0].EF_Image.url
            setState = UserStates.objects.filter(id = setStudent[0].EF_UserStateId)
            if (setState.count() > 0):
                strUserState = setState[0].EF_TypeName 

    jsonDict = {}
    jsonDict["userType"] = strUserType
    jsonDict["userState"] = strUserState
    jsonDict["userOffice"] = strUserOffice
    jsonDict["userPhone"] = strUserPhone
    jsonDict["userImageUrl"] = strImageUrl
    jsonStr = json.dumps(jsonDict, ensure_ascii=False) 

    return JsonResponse(jsonStr, status = 200, safe = False)


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
            arrValidItems = arrValidItems.filter(EF_TeacherId__contains = int(strTeacherId))
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

#副院长接口
class CCollegeLeadersView(Resource):

    def get(self, request):
        strId = request.GET.get("id", "") 
        strUserStateId = request.GET.get("EF_UserStateId", "") 
        strTeacherId = request.GET.get("EF_TeacherId", "") 
        strUserName = request.GET.get("EF_UserName", "") 
        strPassWord = request.GET.get("EF_PassWord", "") 
        strOfficeAddress = request.GET.get("EF_OfficeAddress", "") 
        strPhoneNum = request.GET.get("EF_PhoneNum", "") 
        arrAllItems = CollegeLeaders.objects.all()
        arrValidItems = arrAllItems

        if (strId != ""):
            arrValidItems = arrValidItems.filter(id__contains = int(strId))
        if (strUserStateId != "" and strUserStateId != "0"):
            arrValidItems = arrValidItems.filter(EF_UserStateId__contains = int(strUserStateId))
        if (strTeacherId != "" and strTeacherId != "0"):
            arrValidItems = arrValidItems.filter(EF_TeacherId__contains = int(strTeacherId))
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
        newItem = CollegeLeaders.objects.create(EF_UserStateId = int(strStateId), EF_TeacherId = int(strTeacherId),
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

        curAdmin = CollegeLeaders.objects.get(id = intCurId)
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
        curAdmin = CollegeLeaders.objects.get(id = int(intTypeId))
        curAdmin.delete()
        return HttpResponse(status = 200)

    def to_json(self, objects):
        return serializers.serialize('json', objects)


#教师管理接口
class CTeachersView(Resource):

    def get(self, request):
        strId = request.GET.get("id", "") 
        strUserStateId = request.GET.get("EF_UserStateId", "0") 
        strUserName = request.GET.get("EF_UserName", "") 
        strPassWord = request.GET.get("EF_PassWord", "") 
        strOfficeAddress = request.GET.get("EF_OfficeAddress", "") 
        strPhoneNum = request.GET.get("EF_PhoneNum", "") 
        arrAllItems = Teachers.objects.all()
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
        newItem = Teachers.objects.create(EF_UserStateId = int(strStateId), EF_UserName = strUserName,
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

        curAdmin = Teachers.objects.get(id = intCurId)
        curAdmin.EF_UserStateId = int(strStateId)
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
        curAdmin = Teachers.objects.get(id = int(intTypeId))
        curAdmin.delete()
        return HttpResponse(status = 200)

    def to_json(self, objects):
        return serializers.serialize('json', objects)

#学生管理接口
class CStudentsView(Resource):

    def get(self, request):
        strId = request.GET.get("id", "") 
        strUserStateId = request.GET.get("EF_UserStateId", "0") 
        strTypeId = request.GET.get("EF_TypeId", "0") 
        strTeacherId = request.GET.get("EF_TeacherId", "0") 
        strUserName = request.GET.get("EF_UserName", "") 
        strPassWord = request.GET.get("EF_PassWord", "") 
        arrAllItems = Students.objects.all()
        arrValidItems = arrAllItems

        if (strId != ""):
            arrValidItems = arrValidItems.filter(id__contains = int(strId))
        if (strUserStateId != "" and strUserStateId != "0"):
            arrValidItems = arrValidItems.filter(EF_UserStateId__contains = int(strUserStateId))
        if (strTypeId != "" and strTypeId != "0"):
            arrValidItems = arrValidItems.filter(EF_TypeId__contains = int(strTypeId))
        if (strTeacherId != "" and strTeacherId != "0"):
            arrValidItems = arrValidItems.filter(EF_TeacherId_contains = int(strTypeId))
        if (strUserName != ""):
            arrValidItems = arrValidItems.filter(EF_UserName__contains = strUserName)
        if (strPassWord != ""):
            arrValidItems = arrValidItems.filter(EF_PassWord__contains = strPassWord)

        return HttpResponse(self.to_json(arrValidItems), content_type = 'application/json', status = 200)

    def post(self, request):
        strStateId = request.POST.get("EF_UserStateId", "0") 
        strTypeId = request.POST.get("EF_TypeId", "0") 
        strTeacherId = request.POST.get("EF_TeacherId", "0") 
        strUserName = request.POST.get("EF_UserName", "") 
        strPassWord = request.POST.get("EF_PassWord", "") 
        newItem = Students.objects.create(EF_UserStateId = int(strStateId), EF_TypeId = int(strTypeId),
            EF_TeacherId = int(strTeacherId), EF_UserName = strUserName,EF_PassWord = strPassWord)

        jsonDict = {}
        jsonDict["id"] = newItem.id
        jsonDict["EF_UserStateId"] = int(strStateId)
        jsonDict["EF_TypeId"] = int(strTypeId)
        jsonDict["EF_TeacherId"] = int(strTeacherId)
        jsonDict["EF_UserName"] = strUserName
        jsonDict["EF_PassWord"] = strPassWord

        jsonStr = json.dumps(jsonDict, ensure_ascii=False) 

        return JsonResponse(jsonStr, status = 201, safe=False)

    def put(self, request):
        intCurId = int(request.PUT.get("id"))
        strStateId = request.PUT.get("EF_UserStateId", "0") 
        strTypeId = request.PUT.get("EF_TypeId", "0") 
        strTeacherId = request.PUT.get("EF_TeacherId", "0") 
        strUserName = request.PUT.get("EF_UserName", "") 
        strPassWord = request.PUT.get("EF_PassWord", "") 

        curAdmin = Students.objects.get(id = intCurId)
        curAdmin.EF_UserStateId = int(strStateId)
        curAdmin.EF_TypeId = int(strTypeId)
        curAdmin.EF_TeacherId = int(strTeacherId)
        curAdmin.EF_UserName = strUserName
        curAdmin.EF_PassWord = strPassWord
        curAdmin.save()

        jsonDict = {}
        jsonDict["id"] = intCurId 
        jsonDict["EF_UserStateId"] = strStateId
        jsonDict["EF_TypeId"] = strTypeId
        jsonDict["EF_TeacherId"] = strTeacherId
        jsonDict["EF_UserName"] = strUserName
        jsonDict["EF_PassWord"] = strPassWord

        jsonStr = json.dumps(jsonDict, ensure_ascii=False) 

        return JsonResponse(jsonStr, status = 200, safe = False)

    def delete(self, request, intTypeId):
        curAdmin = Students.objects.get(id = int(intTypeId))
        curAdmin.delete()
        return HttpResponse(status = 200)

    def to_json(self, objects):
        return serializers.serialize('json', objects)


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

