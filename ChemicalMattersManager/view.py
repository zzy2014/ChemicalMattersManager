from django.shortcuts import render
from AppUserManager.models import UserTypes, StudentTypes
 
#主页
def home(request):
    setUserTypes = UserTypes.objects.all().exclude(EF_TypeName = "学生")
    setStudentTypes = StudentTypes.objects.all()

    context = {} #一个字典对象
    context['userTypes_register'] = setUserTypes.exclude(EF_TypeName = "超级管理员") #传入模板中的变量
    context['userTypes_login'] = setUserTypes #传入模板中的变量
    context['studentTypes'] = setStudentTypes #传入模板中的变量

    return render(request, "home.html", context)
