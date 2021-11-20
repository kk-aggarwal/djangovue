import pyodbc
from django import forms

from djangovue.connections import open_db_connection,dictfetchall
from .configuration import ST_CURRENT_YEAR


def verifyPO(val):
    #cursor = con.cursor()
    sql = "select * from validpo where pono=%s" % val
    print(sql)
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    #cursor.execute(sql)
    #c1 = dictfetchall(cursor)
    if len(c1) > 0:
        return True
    else:
        return False
        #raise forms.ValidationError('PO not valid')

def verifyMatgrp(matgrp):
    #cursor = con.cursor()
    sql = "select * from stvalidgroups where groupid=%s"%matgrp
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    #cursor.execute(sql)
    #c1 = dictfetchall(cursor)
    if len(c1) > 0:
        return True
    else:
        return False

def verifyStockNoAgainstStmaster(stockno,txtMatGrp):
    

    if txtMatGrp == 16 or txtMatGrp == 19:
     return  True
    else:
        sql = "Select stockno,des,matgroup,[unit] from stmaster where stockno='%s' and matgroup=%s"%(stockno,txtMatGrp)
        with open_db_connection('edssql') as cursor:
            cursor.execute(sql)
            c1 = dictfetchall(cursor)
        if len(c1)>0:
            return True
        else:
            return False

def verifyStocknoAgainstPO(stockno,finyear,matgrp,mislipno):
    
    if matgrp == 16 or matgrp == 19 or matgrp == 27:
        return True

    else:
        sql="select pono from mislip where finyear='%s' and matgrp=%s and mislipno=%s"%(finyear,matgrp,mislipno)
        with open_db_connection('incomingstore') as cursor:
            cursor.execute(sql)
            c1 = dictfetchall(cursor)
        pono=c1[0]['pono']
        print(stockno)
        sql = "Select poitems.stockno,poitems.des,poitems.[unit]  from dbo.validPOview INNER JOIN dbo.POItems ON dbo.validPOview.POID = dbo.POItems.POID where validpoview.pono=%s and  stockno='%s'"%(pono,stockno)
        with open_db_connection('edssql') as cursor:
            cursor.execute(sql)
            c2 = dictfetchall(cursor)
        print(c2)
        if len(c2)>0:
            return True
        else:
            return False


def grcchoices():
    #cursor = conInStr.cursor()
    stCurrentYear = ST_CURRENT_YEAR
    sql = "SELECT FinYear, FrghtPayMode, GRCDate, GRCNo, GRDate, GRNo, StnChnDate, StnChnNo, StnFrom, StnTo, TrName, WtAct, WtCharged, WtUnit, SuppName, PoNo, MprNo, Misc, NoOfCases, des, CasesRec FROM Grc WHERE (FinYear = '%s') ORDER BY GRCNo"%stCurrentYear
    with open_db_connection('incomingstore') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    #cursor.execute(sql)
    #c1 = dictfetchall(cursor)
    grcs =[(d['grcno'],d['grcno']) for d in c1]
    grcs.insert(0,('0',0))
    return grcs
def mrrchoices(finyear):
    #cursor = conInStr.cursor()
    stCurrentYear=ST_CURRENT_YEAR
    print(finyear)
    sql = "SELECT mrrno,des FROM mrr WHERE (FinYear = '%s') ORDER BY mrrNo"%finyear
    with open_db_connection('incomingstore') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    #cursor.execute(sql)
    #c1 = dictfetchall(cursor)

    return [(d['mrrno'],str(d['mrrno'])+": "+d["des"]) for d in c1]

def update_values_of_query(form,request):
    self=form

    set = ''
    for f in self.changed_data:
        if set == '':
            if isinstance(self.cleaned_data[f], str):
                set = set + f + "='%s'" % self.cleaned_data[f]
            elif isinstance(self.cleaned_data[f], bool):
                set = set + f + "=%d" % self.cleaned_data[f]
            else:
                set = set + f + '=%r' % self.cleaned_data[f]
        else:
            if isinstance(self.cleaned_data[f], str):
                set = set + ',' + f + "='%s'" % self.cleaned_data[f]
            elif isinstance(self.cleaned_data[f], bool):
                set = set + ',' + f + "=%d" % self.cleaned_data[f]
            else:
                set = set + ',' + f + '=%r' % self.cleaned_data[f]
    set=set+",username='%s'"%request.user.username
    return set
def insert_values_of_query(form,request):
    self=form
    print(self.fields)
    selffields=self.fields.copy()
    fields = ','.join(self.fields)
    print(fields)
    v = ''
    for f in self.fields:
        # print(f)
        if self.cleaned_data[f]!=None:
            if v == '':
                if isinstance(self.cleaned_data[f], str):
                    v = v + "'%s'" % self.cleaned_data[f]
                elif isinstance(self.cleaned_data[f], bool):
                    v = v + "%d" % self.cleaned_data[f]
                else:
                    v = v + "%r" % self.cleaned_data[f]
            else:
                if isinstance(self.cleaned_data[f], str):
                    v = v + ",'%s'" % self.cleaned_data[f]
                elif isinstance(self.cleaned_data[f], bool):
                    v = v + ",%d" % self.cleaned_data[f]
                else:
                    v = v + ",%r" % self.cleaned_data[f]
        else:
            selffields.pop(f)
    fields= ','.join(selffields)
    fields=fields+',username'
    v=v+",'%s'"%request.user.username
    return fields,v

def runQuery(database,sql):
    data={}
    #databases={'edssql':settings.CON,'incomingstore':settings.CONINSTR}
    #con=databases[database]
    #cursor = con.cursor()
    try:
        print(sql)

        with open_db_connection(database,True) as cursor:
            rowcount=cursor.execute(sql).rowcount
            if cursor.description==None:
                c1=None
            else:
                c1 = dictfetchall(cursor)
        #cursor.execute(sql)
        #con.commit()

        data['success']=True
        data['exception']=''
        data['cursor']=c1
        return data
    except pyodbc.DatabaseError as e:
        print(e)
        data['success'] = False
        data['exception'] = e.__str__()
        return data

