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
    EF_UserStateId = models.IntegerField(default=0)
    EF_UserName = models.CharField(max_length=30)
    EF_PassWord = models.CharField(max_length=30)
    EF_OfficeAddress = models.TextField(default="")
    EF_PhoneNum = models.CharField(max_length=15, default="")
    def __str__(self):
        return self.EF_UserName


#管理员
class Administrators(models.Model):
    EF_UserStateId = models.IntegerField(default=1)
    EF_UserName = models.CharField(max_length=30)
    EF_PassWord = models.CharField(max_length=30)
    EF_OfficeAddress = models.TextField(default="")
    EF_PhoneNum = models.CharField(max_length=15, default="")
    def __str__(self):
        return self.EF_UserName


#院长
class ChiefCollegeLeaders(models.Model):
    EF_UserStateId = models.IntegerField(default=0)
    EF_TeacherId = models.IntegerField(default=0)
    EF_UserName = models.CharField(max_length=30)
    EF_PassWord = models.CharField(max_length=30)
    EF_OfficeAddress = models.TextField(default="")
    EF_PhoneNum = models.CharField(max_length=15, default="")
    def __str__(self):
        return self.EF_UserName


#副院长
class CollegeLeaders(models.Model):
    EF_UserStateId = models.IntegerField(default=1)
    EF_TeacherId = models.IntegerField(default=0)
    EF_UserName = models.CharField(max_length=30)
    EF_PassWord = models.CharField(max_length=30)
    EF_OfficeAddress = models.TextField(default="")
    EF_PhoneNum = models.CharField(max_length=15,default="")
    def __str__(self):
        return self.EF_UserName


#教师
class Teachers(models.Model):
    EF_UserStateId = models.IntegerField(default=0)
    EF_FinancialId = models.IntegerField(default=0)
    EF_UserName = models.CharField(max_length=30)
    EF_PassWord = models.CharField(max_length=30)
    EF_OfficeAddress = models.TextField(default="")
    EF_PhoneNum = models.CharField(max_length=15, default="")
    def __str__(self):
        return self.EF_UserName


#经费
class Finances(models.Model):
    EF_Name = models.CharField(max_length=30,default="")
    EF_TotalAmount = models.FloatField(default=0.0)
    def __str__(self):
        return self.EF_Name


#学生类型
class StudentTypes(models.Model):
    EF_TypeName = models.CharField(max_length=30)
    def __str__(self):
        return self.EF_TypeName


#学生
class Students(models.Model):
    EF_UserStateId = models.IntegerField(default=0)
    EF_TypeId = models.IntegerField(default=0)
    EF_TeacherId = models.IntegerField(default=0)
    EF_UserName = models.CharField(max_length=30)
    EF_PassWord = models.CharField(max_length=30)
    def __str__(self):
        return self.EF_UserName

