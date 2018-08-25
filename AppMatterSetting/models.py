from django.db import models

#计量单位
class MatterUnits(models.Model):
    EF_UnitName = models.CharField(max_length=30)
    def __str__(self):
        return self.EF_UnitName


#理化状态
class MatterStates(models.Model):
    EF_StateName = models.CharField(max_length=30)
    def __str__(self):
        return self.EF_StateName


#纯度规格
class PurityLevels(models.Model):
    EF_LevelName = models.CharField(max_length=30)
    def __str__(self):
        return self.EF_LevelName


#药品类别
class MatterTypes(models.Model):
    EF_TypeName = models.CharField(max_length=30)
    def __str__(self):
        return self.EF_TypeName


#药品仓库
class StoreRooms(models.Model):
    EF_RoomName = models.CharField(max_length=30)
    def __str__(self):
        return self.EF_RoomName


#药品
class Matters(models.Model):
    EF_TypeId = models.IntegerField(default=0)
    EF_StateId = models.IntegerField(default=0)
    EF_PurityId = models.IntegerField(default=0)
    EF_UnitId = models.IntegerField(default=0)
    EF_StoreId = models.IntegerField(default=0)
    EF_Name = models.CharField(max_length=100)
    EF_CAS = models.CharField(max_length=100)
    EF_Format = models.CharField(max_length=100)
    EF_Amount = models.IntegerField(default=0)
    EF_Price = models.FloatField(default=0.0)
    EF_Location = models.CharField(max_length=100)
    EF_Saler = models.CharField(max_length=30)
    EF_Note = models.CharField(max_length=30)
    def __str__(self):
        return self.EF_Name


#存量预警
class MatterAlerts(models.Model):
    EF_MatterId = models.IntegerField(default=0)
    EF_YellowAmount = models.IntegerField(default=0)
    EF_RedAmount = models.IntegerField(default=0)
    def __str__(self):
        return "Alert"

#药品领取时最低值，在有权限的情况下，若其领取后库存数量低于此值，则本次领取无效
class MatterMinRemains(models.Model):
    EF_MatterId = models.IntegerField(default=0)
    EF_StudentTypeId = models.IntegerField(default=0)
    EF_MinRemain = models.IntegerField(default=0)
    def __str__(self):
        return "Alert"

#药品不能领取的的配置
class MatterAccessBlocks(models.Model):
    EF_MatterId = models.IntegerField(default=0)
    EF_StudentTypeId = models.IntegerField(default=0)
    EF_StudentId = models.IntegerField(default=0) #此值为空则表示此类型下的学生均无权限，否则只对该学生设置

