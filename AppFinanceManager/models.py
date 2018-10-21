from django.db import models

#经费
class Finances(models.Model):
    EF_Name = models.CharField(max_length=30,default="")
    EF_TotalAmount = models.FloatField(default=0.0)
    EF_TeacherId = models.IntegerField(default=0)
    def __str__(self):
        return self.EF_Name

