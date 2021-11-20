from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError

# Create your models here.
class Operation(models.Model):
    dno=models.IntegerField(verbose_name="d no")
    drwgno=models.CharField(max_length=50,verbose_name="Drawing no")
    itemno=models.IntegerField(verbose_name="item no")
    opno=models.CharField(max_length=10,verbose_name="operation no")
    dated=models.DateTimeField(auto_now_add=True)
    status=models.BooleanField(verbose_name='St Auth',default=False)
    #remarks=models.TextField(default='',blank=True,null=True)
    #PDC=models.DateField(blank=True,null=True)
    
    def get_absolute_url(self):
        return reverse('operation',self.id)
    class Meta:
        db_table="epfo_operation"

class OlItemStatus(models.Model):
    dno = models.IntegerField(verbose_name="d no")
    drwgno = models.CharField(max_length=50, verbose_name="Drawing no")
    itemno = models.IntegerField(verbose_name="item no")
    remarks=models.TextField(default='',blank=True,null=True)
    PDC=models.DateField(blank=True,null=True)

    def get_absolute_url(self):
        return reverse('olitemstatus', self.id)
    class Meta:
        db_table="epfo_olitemstatus"