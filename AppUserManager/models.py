from django.db import models

#用户类型
class UserTypes(models.Model):
    EF_TypeName = models.CharField(max_length=30, default="")
    def __str__(self):
        return self.EF_TypeName

#用户状态
#在线、离线、禁用等
class UserStates(models.Model):
    EF_TypeName = models.CharField(max_length=30, default="离线")
    def __str__(self):
        return self.EF_TypeName


#超级管理员
class SuperAdministrators(models.Model):
    Type = "超级管理员"
    EF_UserStateId = models.IntegerField(default=0)
    EF_UserName = models.CharField(max_length=30)
    EF_PassWord = models.CharField(max_length=30)
    EF_OfficeAddress = models.TextField(default="")
    EF_PhoneNum = models.CharField(max_length=15, default="")
    EF_Image = models.ImageField(upload_to='userImage/superAdminImage', default="userImage/superAdminImage/defalut.png")
    def __str__(self):
        return self.EF_UserName


#管理员
class Administrators(models.Model):
    Type = "管理员"
    EF_UserStateId = models.IntegerField(default=1)
    EF_UserName = models.CharField(max_length=30)
    EF_PassWord = models.CharField(max_length=30)
    EF_OfficeAddress = models.TextField(default="")
    EF_PhoneNum = models.CharField(max_length=15, default="")
    EF_Image = models.ImageField(upload_to='userImage/adminImage', default="userImage/adminImage/defalut.png")
    def __str__(self):
        return self.EF_UserName


#院长
class ChiefCollegeLeaders(models.Model):
    Type = "院长"
    EF_UserStateId = models.IntegerField(default=0)
    EF_TeacherId = models.IntegerField(default=0)
    EF_UserName = models.CharField(max_length=30)
    EF_PassWord = models.CharField(max_length=30)
    EF_OfficeAddress = models.TextField(default="")
    EF_PhoneNum = models.CharField(max_length=15, default="")
    EF_Image = models.ImageField(upload_to='userImage/chiefLeaderImage', default="userImage/chiefLeaderImage/defalut.png")
    def __str__(self):
        return self.EF_UserName


#副院长
class CollegeLeaders(models.Model):
    Type = "副院长"
    EF_UserStateId = models.IntegerField(default=1)
    EF_TeacherId = models.IntegerField(default=0)
    EF_UserName = models.CharField(max_length=30)
    EF_PassWord = models.CharField(max_length=30)
    EF_OfficeAddress = models.TextField(default="")
    EF_PhoneNum = models.CharField(max_length=15,default="")
    EF_Image = models.ImageField(upload_to='userImage/leaderImage', default="userImage/leaderImage/defalut.png")
    def __str__(self):
        return self.EF_UserName


#教师
class Teachers(models.Model):
    Type = "教师"
    EF_UserStateId = models.IntegerField(default=0)
    EF_UserName = models.CharField(max_length=30)
    EF_PassWord = models.CharField(max_length=30)
    EF_OfficeAddress = models.TextField(default="")
    EF_PhoneNum = models.CharField(max_length=15, default="")
    EF_Image = models.ImageField(upload_to='userImage/teacherImage', default="userImage/teacherImage/defalut.png")
    def __str__(self):
        return self.EF_UserName

#学生类型
class StudentTypes(models.Model):
    EF_TypeName = models.CharField(max_length=30)
    def __str__(self):
        return self.EF_TypeName


#学生
class Students(models.Model):
    Type = "学生"
    EF_UserStateId = models.IntegerField(default=0)
    EF_TypeId = models.IntegerField(default=0)
    EF_TeacherId = models.IntegerField(default=0)
    EF_UserName = models.CharField(max_length=30)
    EF_PassWord = models.CharField(max_length=30)
    EF_OfficeAddress = models.TextField(default="")
    EF_PhoneNum = models.CharField(max_length=15, default="")
    EF_Image = models.ImageField(upload_to='userImage/studentImage', default="userImage/studentImage/defalut.png")
    def __str__(self):
        return self.EF_UserName

