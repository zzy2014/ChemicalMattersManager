from django.db import models

#审核状态，通过，取消，未通过等下拉框式
class CensoreStates(models.Model):
    EF_States = models.CharField(max_length=30)
    def __str__(self):
        return self.EF_States;

#审核流程, 最多也就三步审核，当提交订单时根据计算出的审核流程Id，提供用户选择审核人
class CensorePatterns(models.Model):
    EF_StepsCount = models.IntegerField(default=0)
    EF_UserTypeId1 = models.IntegerField(default=0)
    EF_UserTypeId2 = models.IntegerField(default=0)
    EF_UserTypeId3 = models.IntegerField(default=0)


#单据状态，己生效，审核中，己审核，己完成
class FormStates(models.Model):
    EF_StateName = models.CharField(max_length=30)
    def __str__(self):
        return self.EF_StateName

#入库表单
class ImportForms(models.Model):
    EF_UserId = models.IntegerField(default=0)
    EF_FormStateId = models.IntegerField(default=0)
    EF_MatterDetailId = models.IntegerField(default=0)
    EF_Time = models.DateTimeField(default=0)
    #以下为审核的流程和结果
    EF_CensorePatternId = models.IntegerField(default=0)
    EF_UserId1 = models.IntegerField(default=0)
    EF_CensoreStateId1 = models.IntegerField(default=0)
    EF_CensoreComment1 = models.CharField(max_length=255, default="")
    EF_UserId2 = models.IntegerField(default=0)
    EF_CensoreStateId2 = models.IntegerField(default=0)
    EF_CensoreComment2 = models.CharField(max_length=255, default="")
    EF_UserId3 = models.IntegerField(default=0)
    EF_CensoreStateId3 = models.IntegerField(default=0)
    EF_CensoreComment3 = models.CharField(max_length=255, default="")


#入库表单中的所有药品信息
class MatterDetails(models.Model):
    EF_ImportMatterId = models.IntegerField(default=0)
    EF_MatterId = models.IntegerField(default=0)
    EF_MatterCount = models.IntegerField(default=0)
